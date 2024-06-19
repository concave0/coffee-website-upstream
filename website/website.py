class WebsiteSchema(): 
  def __init__(self):
    self.hashmap: dict = {}
    self.hashmap["homepage"] = open("routes/templates/index.html","r").read()
    self.hashmap["data_sources"] = open("routes/templates/data_sources.html","r").read()
    self.hashmap["was_it_a_match"] = open("routes/templates/was_it_a_match.html", "r").read()
    self.hashmap["four_o_four"] = open("routes/templates/four_o_four.html").read()
    

  
    
    