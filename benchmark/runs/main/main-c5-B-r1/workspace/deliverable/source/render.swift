import Cocoa
// usage: render scene.json out.pdf png_prefix
let a = CommandLine.arguments
let data = try! Data(contentsOf: URL(fileURLWithPath: a[1]))
let scene = try! JSONSerialization.jsonObject(with: data) as! [String: Any]
let W = CGFloat(scene["w"] as! Double), H = CGFloat(scene["h"] as! Double)
let pages = scene["pages"] as! [[[String: Any]]]
let fontNames = ["R":"HelveticaNeue","B":"HelveticaNeue-Bold","M":"HelveticaNeue-Medium","I":"HelveticaNeue-Italic","L":"HelveticaNeue-Light","BI":"HelveticaNeue-BoldItalic"]
func col(_ s: Any?) -> NSColor? {
  guard var h = s as? String, h != "none" else { return nil }
  if h.hasPrefix("#") { h.removeFirst() }
  var v: UInt64 = 0; Scanner(string: h).scanHexInt64(&v)
  return NSColor(srgbRed: CGFloat((v>>16)&255)/255, green: CGFloat((v>>8)&255)/255, blue: CGFloat(v&255)/255, alpha: 1)
}
func num(_ d: [String:Any], _ k: String, _ def: CGFloat = 0) -> CGFloat { if let v = d[k] as? Double { return CGFloat(v) }; if let v = d[k] as? Int { return CGFloat(v) }; return def }
func attr(_ e: [String:Any]) -> NSAttributedString {
  let out = NSMutableAttributedString()
  let ps = NSMutableParagraphStyle()
  let align = e["align"] as? String ?? "left"
  ps.alignment = align == "center" ? .center : (align == "right" ? .right : .left)
  let size = num(e, "size", 14)
  ps.lineHeightMultiple = num(e, "lh", 1.15)
  ps.paragraphSpacing = num(e, "ps", 0)
  let ind = num(e, "indent", 0)
  if ind > 0 { ps.headIndent = ind; ps.tabStops = [NSTextTab(textAlignment: .left, location: ind)]; ps.defaultTabInterval = ind }
  let runs: [[String:Any]] = (e["runs"] as? [[String:Any]]) ?? [["t": e["t"] ?? ""]]
  for r in runs {
    let f = NSFont(name: fontNames[(r["f"] as? String) ?? (e["f"] as? String ?? "R")]!, size: (r["size"] as? Double).map{CGFloat($0)} ?? size)!
    let c = col(r["c"] ?? e["c"] ?? "#0b0b0b")!
    out.append(NSAttributedString(string: r["t"] as! String, attributes: [.font: f, .foregroundColor: c, .paragraphStyle: ps]))
  }
  return out
}
func drawPage(_ els: [[String:Any]], _ ctx: CGContext, _ pi: Int) {
  for e in els {
    let t = e["type"] as! String
    ctx.saveGState()
    if let o = e["op"] as? Double { ctx.setAlpha(CGFloat(o)) }
    switch t {
    case "rect":
      let r = CGRect(x: num(e,"x"), y: num(e,"y"), width: num(e,"w"), height: num(e,"h"))
      let rad = num(e,"r")
      var path: CGPath
      if let corners = e["corners"] as? String, rad > 0 { // "top" or "right" or "bottom" or "left"
        let p = CGMutablePath(); let x0=r.minX,x1=r.maxX,y0=r.minY,y1=r.maxY
        let tl = corners.contains("t") || corners.contains("l") ? (corners=="top"||corners=="left" ? rad:0):0
        let tr = (corners=="top"||corners=="right") ? rad:0
        let br = (corners=="bottom"||corners=="right") ? rad:0
        let bl = (corners=="bottom"||corners=="left") ? rad:0
        p.move(to: CGPoint(x:x0+tl,y:y0)); p.addLine(to: CGPoint(x:x1-tr,y:y0))
        if tr>0 { p.addArc(tangent1End: CGPoint(x:x1,y:y0), tangent2End: CGPoint(x:x1,y:y0+tr), radius: tr) }
        p.addLine(to: CGPoint(x:x1,y:y1-br)); if br>0 { p.addArc(tangent1End: CGPoint(x:x1,y:y1), tangent2End: CGPoint(x:x1-br,y:y1), radius: br) }
        p.addLine(to: CGPoint(x:x0+bl,y:y1)); if bl>0 { p.addArc(tangent1End: CGPoint(x:x0,y:y1), tangent2End: CGPoint(x:x0,y:y1-bl), radius: bl) }
        p.addLine(to: CGPoint(x:x0,y:y0+tl)); if tl>0 { p.addArc(tangent1End: CGPoint(x:x0,y:y0), tangent2End: CGPoint(x:x0+tl,y:y0), radius: tl) }
        p.closeSubpath(); path = p
      } else { path = CGPath(roundedRect: r, cornerWidth: min(rad, r.width/2), cornerHeight: min(rad, r.height/2), transform: nil) }
      if let f = col(e["fill"]) { ctx.addPath(path); ctx.setFillColor(f.cgColor); ctx.fillPath() }
      if let s = col(e["stroke"]) { ctx.addPath(path); ctx.setStrokeColor(s.cgColor); ctx.setLineWidth(num(e,"sw",1)); ctx.strokePath() }
    case "line", "poly":
      var pts: [CGPoint] = []
      if t == "line" { pts = [CGPoint(x:num(e,"x1"),y:num(e,"y1")), CGPoint(x:num(e,"x2"),y:num(e,"y2"))] }
      else { pts = (e["pts"] as! [[Double]]).map { CGPoint(x:$0[0], y:$0[1]) } }
      ctx.setLineCap(.round); ctx.setLineJoin(.round)
      ctx.addLines(between: pts)
      if let f = col(e["fill"]) { ctx.closePath(); ctx.setFillColor(f.cgColor); ctx.fillPath(); ctx.addLines(between: pts) }
      if let s = col(e["stroke"]) { ctx.setStrokeColor(s.cgColor); ctx.setLineWidth(num(e,"sw",1))
        if let d = e["dash"] as? [Double] { ctx.setLineDash(phase: 0, lengths: d.map{CGFloat($0)}) }
        ctx.strokePath() }
    case "circle":
      let r = CGRect(x: num(e,"cx")-num(e,"r"), y: num(e,"cy")-num(e,"r"), width: 2*num(e,"r"), height: 2*num(e,"r"))
      if let s = col(e["ring"]) { ctx.setFillColor(s.cgColor); ctx.fillEllipse(in: r.insetBy(dx: -2, dy: -2)) }
      if let f = col(e["fill"]) { ctx.setFillColor(f.cgColor); ctx.fillEllipse(in: r) }
      if let s = col(e["stroke"]) { ctx.setStrokeColor(s.cgColor); ctx.setLineWidth(num(e,"sw",1)); ctx.strokeEllipse(in: r) }
    case "text":
      let s = attr(e)
      let w = num(e,"w",1000), h = num(e,"h",0)
      let br = s.boundingRect(with: CGSize(width: w, height: 10000), options: [.usesLineFragmentOrigin, .usesFontLeading])
      var y = num(e,"y")
      if h > 0 {
        if br.height > h + 1 { let txt = s.string.prefix(50).replacingOccurrences(of: "\n", with: " "); print("OVERFLOW p\(pi+1): need \(Int(br.height)) have \(Int(h)) :: \(txt)") }
        let va = e["va"] as? String ?? "top"
        if va == "middle" { y += (h - br.height)/2 } else if va == "bottom" { y += h - br.height }
      }
      if let rot = e["rot"] as? Double {
        ctx.translateBy(x: num(e,"x"), y: y); ctx.rotate(by: CGFloat(rot) * .pi/180)
        s.draw(with: CGRect(x: 0, y: 0, width: w, height: 10000), options: [.usesLineFragmentOrigin, .usesFontLeading])
      } else {
        s.draw(with: CGRect(x: num(e,"x"), y: y, width: w, height: 10000), options: [.usesLineFragmentOrigin, .usesFontLeading])
      }
    default: break
    }
    ctx.restoreGState()
  }
}
var box = CGRect(x:0,y:0,width:W,height:H)
let pdf = CGContext(URL(fileURLWithPath: a[2]) as CFURL, mediaBox: &box, nil)!
for (i, els) in pages.enumerated() {
  pdf.beginPDFPage(nil)
  pdf.saveGState(); pdf.translateBy(x: 0, y: H); pdf.scaleBy(x: 1, y: -1)
  NSGraphicsContext.current = NSGraphicsContext(cgContext: pdf, flipped: true)
  drawPage(els, pdf, i)
  pdf.restoreGState(); pdf.endPDFPage()
  if a.count > 3 {
    let sc: CGFloat = 1.0
    let cs = CGColorSpace(name: CGColorSpace.sRGB)!
    let bm = CGContext(data: nil, width: Int(W*sc), height: Int(H*sc), bitsPerComponent: 8, bytesPerRow: 0, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    bm.translateBy(x: 0, y: H*sc); bm.scaleBy(x: sc, y: -sc)
    NSGraphicsContext.current = NSGraphicsContext(cgContext: bm, flipped: true)
    drawPage(els, bm, -1000)
    let rep = NSBitmapImageRep(cgImage: bm.makeImage()!)
    try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[3] + String(format: "%02d.png", i+1)))
  }
}
pdf.closePDF()
print("rendered \(pages.count) pages")
