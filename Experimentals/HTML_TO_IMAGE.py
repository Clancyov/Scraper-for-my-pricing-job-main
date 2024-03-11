from html2image import Html2Image

html="<html><head></head><body><p>سلامی به شما دوستان، در اینجا قیمت انواع ماشین ها را هر روز ذکر خواهیم کرد.</p></body></html>"
css="body{background-color:green;}"

hti=Html2Image()
hti.screenshot(html_str=html,css_str=css,save_as="test1-html-to-image.png",size=(1080,1080))