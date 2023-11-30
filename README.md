./src/auto-ntzfind.py
    -- creates Life 1.05 files in golly folder

automons.py
    -- run in golly to create rles of Life 1.05 files

./src/rle2apgcode.py
    -- reads rles from golly
    -- loads rule using lifelib
    -- gets the apgcode of that rle/rule
    -- creates the qr code
    -- saves the qr codes and patterns.json

./src/combiner.py
    -- combines automon gifs and qr codes with card
    -- saves them to /cardFronts/ and /cardBacks/
    -- saves them in sheets
    -- creates patterns.json
                { rle : rle,
                  rule : rule,
                  apgcode : apgcode,
                  url : url }
