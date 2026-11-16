import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers
let args=CommandLine.arguments
let data=try! Data(contentsOf:URL(fileURLWithPath:args[1]))
let slides=try! JSONSerialization.jsonObject(with:data) as! [[[String:Any]]]
let outdir=args[2]
let SW=960.0, SH=540.0, SC=2.0
func hex(_ s:String)->CGColor{ let v=UInt32(s,radix:16) ?? 0
  return CGColor(red:CGFloat((v>>16)&255)/255,green:CGFloat((v>>8)&255)/255,blue:CGFloat(v&255)/255,alpha:1)}
func d(_ a:Any?)->CGFloat{ return CGFloat((a as? Double) ?? Double((a as? Int) ?? 0)) }
var report=""
let pdfMode = args.count>3
var pdfCtx:CGContext? = nil
var mbox=CGRect(x:0,y:0,width:SW,height:SH)
if pdfMode { pdfCtx=CGContext(URL(fileURLWithPath:args[3]) as CFURL, mediaBox:&mbox, nil) }
for (si,items) in slides.enumerated(){
  let cs=CGColorSpaceCreateDeviceRGB()
  let ctx:CGContext
  if pdfMode { ctx=pdfCtx!; ctx.beginPDFPage(nil) } else {
  ctx=CGContext(data:nil,width:Int(SW*SC),height:Int(SH*SC),bitsPerComponent:8,bytesPerRow:0,space:cs,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
  ctx.scaleBy(x:SC,y:SC) }
  ctx.setFillColor(hex("FFFFFF")); ctx.fill(CGRect(x:0,y:0,width:SW,height:SH))
  // flip helper: y_top -> CG y
  for it in items{
    let kind=it["kind"] as! String
    let x=d(it["x"]), y=d(it["y"]), w=d(it["w"]), h=d(it["h"])
    let r=CGRect(x:x,y:SH-y-h,width:w,height:h)
    if kind=="line"{
      ctx.setStrokeColor(hex(it["color"] as! String)); ctx.setLineWidth(d(it["lw"])); ctx.setLineCap(.round)
      ctx.move(to:CGPoint(x:d(it["x1"]),y:SH-d(it["y1"]))); ctx.addLine(to:CGPoint(x:d(it["x2"]),y:SH-d(it["y2"]))); ctx.strokePath()
      continue
    }
    if kind != "text"{
      let p:CGPath
      if kind=="oval"{ p=CGPath(ellipseIn:r,transform:nil)}
      else if kind=="rrect"{ let rr=min(w,h)*0.3; p=CGPath(roundedRect:r,cornerWidth:rr,cornerHeight:rr,transform:nil)}
      else { p=CGPath(rect:r,transform:nil)}
      if let f=it["fill"] as? String { ctx.setFillColor(hex(f)); ctx.addPath(p); ctx.fillPath() }
      if let s=it["stroke"] as? String { ctx.setStrokeColor(hex(s)); ctx.setLineWidth(d(it["slw"])); ctx.addPath(p); ctx.strokePath() }
    }
    if let t=it["text"] as? [String:Any]{
      let paras=t["paras"] as! [[String:Any]]
      let ms=NSMutableAttributedString()
      for (pi,p) in paras.enumerated(){
        let runs=p["runs"] as! [[String:Any]]
        var align=CTTextAlignment.left
        if (p["align"] as! String)=="center"{align = .center}; if (p["align"] as! String)=="right"{align = .right}
        var lhm=CGFloat(d(p["ls"]))*1.0
        var sb=CGFloat(d(p["sb"]))
        let bul=(p["bullet"] as? Bool) ?? false
        var ind=CGFloat(d(p["ind"])); var first:CGFloat = bul ? 0 : ind
        var tabs=[CTTextTabCreate(.left, Double(ind), nil)] as CFArray
        let settings=[
          CTParagraphStyleSetting(spec:.alignment,valueSize:MemoryLayout<CTTextAlignment>.size,value:&align),
          CTParagraphStyleSetting(spec:.lineHeightMultiple,valueSize:MemoryLayout<CGFloat>.size,value:&lhm),
          CTParagraphStyleSetting(spec:.paragraphSpacingBefore,valueSize:MemoryLayout<CGFloat>.size,value:&sb),
          CTParagraphStyleSetting(spec:.headIndent,valueSize:MemoryLayout<CGFloat>.size,value:&ind),
          CTParagraphStyleSetting(spec:.firstLineHeadIndent,valueSize:MemoryLayout<CGFloat>.size,value:&first),
          CTParagraphStyleSetting(spec:.tabStops,valueSize:MemoryLayout<CFArray>.size,value:&tabs)]
        let ps=CTParagraphStyleCreate(settings,settings.count)
        var idx=0
        for rn in runs{
          var s=rn["t"] as! String
          if idx==0 && bul { s="•\t"+s }
          if idx==runs.count-1 && pi<paras.count-1 { s+="\n" }
          let b=(rn["b"] as? Bool) ?? false, i=(rn["i"] as? Bool) ?? false
          let name = b ? (i ? "Arial-BoldItalicMT":"Arial-BoldMT") : (i ? "Arial-ItalicMT":"ArialMT")
          let f=CTFontCreateWithName(name as CFString, d(rn["s"]), nil)
          ms.append(NSAttributedString(string:s,attributes:[
            NSAttributedString.Key(kCTFontAttributeName as String):f,
            NSAttributedString.Key(kCTForegroundColorAttributeName as String):hex(rn["c"] as! String),
            NSAttributedString.Key(kCTParagraphStyleAttributeName as String):ps]))
          idx+=1
        }
      }
      let fs=CTFramesetterCreateWithAttributedString(ms)
      let ml=d(t["ml"]), mr=d(t["mr"]), mt=d(t["mt"]), mb=d(t["mb"])
      let iw=w-ml-mr, ih=h-mt-mb
      let sz=CTFramesetterSuggestFrameSizeWithConstraints(fs,CFRange(location:0,length:0),nil,CGSize(width:iw,height:10000),nil)
      let anchor=t["anchor"] as! String
      var top=y+mt
      if anchor=="middle"{ top=y+mt+(ih-sz.height)/2 } else if anchor=="bottom"{ top=y+h-mb-sz.height }
      if sz.height>ih+1.0 { report+="slide \(si+1): overflow \(Int(sz.height))>\(Int(ih))pt: \(String(ms.string.prefix(50)))\n"; if anchor != "top" {top=y+mt} }
      let path=CGPath(rect:CGRect(x:x+ml,y:SH-top-sz.height-2,width:iw,height:sz.height+2),transform:nil)
      let fr=CTFramesetterCreateFrame(fs,CFRange(location:0,length:0),path,nil)
      CTFrameDraw(fr,ctx)
    }
  }
  if pdfMode { ctx.endPDFPage(); continue }
  let img=ctx.makeImage()!
  let url=URL(fileURLWithPath:"\(outdir)/s\(String(format:"%02d",si+1)).png")
  let dest=CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString,1,nil)!
  CGImageDestinationAddImage(dest,img,nil); CGImageDestinationFinalize(dest)
}
if pdfMode { pdfCtx!.closePDF() }
print(report.isEmpty ? "no overflow" : report)
