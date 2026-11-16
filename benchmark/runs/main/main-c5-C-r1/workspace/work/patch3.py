p='build_spec.py'; s=open(p).read()
R=[('LM("Under either reading of the $9.5M, the runway rule breaks before the stores can prove themselves",\n                     nums=[("$9.5M", "need")])',
    'LM("Under either reading of the plan\'s cash need, the runway rule breaks before the stores can prove themselves")'),
   ('"Quick commerce grows fast, but its operators lose money; the one profitable city got there by charging more"','"Quick commerce grows fast, but its operators lose money on every order"'),
   ('"A median dark store loses $6.2 an order; the founders\' profit needs inputs above the best site observed"','"A median dark store loses $6.2 an order; the plan needs inputs no site has reached"'),
   ('"Parcelbird\'s pop-up ran below the benchmark, and too few customers stayed to repay their acquisition"','"Parcelbird\'s own pop-up ran below the benchmark, and few customers stayed"'),
   ('"The plan needs $9.5M, but Parcelbird can spend only $7.2M and keep 12 months of runway"','"The plan needs $9.5M, but only $7.2M can be spent within the runway rule"'),
   ('"Grow the software business instead, and revisit Parcelbird Now only if a real site passes four gates"','"Grow the software business instead; revisit only if a real site passes four gates"'),
   ('no observed dark store makes money and the plan breaks the runway rule; grow the software instead"','dark stores lose money and the plan breaks the runway rule; grow the software instead"'),
]
for a,b in R:
    assert a in s, a[:70]
    s=s.replace(a,b)
open(p,'w').write(s); print('ok')
