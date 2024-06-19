

# Documentation 

## Dynamic Text Rendering in HMTL Custom Solution  

### Since you had a harder time getting the traditional templates that FastAPI provided to dynamically provide text through its text display engine (text from your endpoint being displayed on the user browser) you had to create your own.

<br>

### It loads each webpage into a hashmap as a string and with a template.render() it will map whatever variable you have in your HMTL that looks like this {{ example variable }} to whatever you put inside of template.render(). This way you can dynamically load input. 





