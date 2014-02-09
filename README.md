Gooey
=====

(image)

Turn (almost) any command line program into a full GUI application with one line  

What is it? 
-----------  

Gooey converts your Console Applications into end-user friendly GUI applications. It lets you focus on building robust, configurable programs without having to worry about how it will be presented to and interacted with by your average non-techie person. 

Why?
---  

Because as much as we love the command prompt, the rest of the world looks at it like some horrific relic from the '80s. As I embarked in the world of freelancing, I wanted to deliver something a little more polished than a black box with white text, and something which was easily understandable and configurable to the end-user. 

How does it work? 
------------------  

Gooey is attached to your code via a simple decorator on your `main` method. 

    @gooey      <--- all it takes! :)
    def main():
      # rest of code

At runtime, it loads the Abstract Syntax Tree of your module and parses it for all references to `ArgumentParser` (The older `optparse` is currently not supported). These references are then extracted and assigned a `component type` based on the function they provide. 

Currently, the `ArgumentParser._actions` are mapped to the following components. 

| Action                |       WxWidget     |
|:----------------------|-----------|
| store  |  TextCtrl |
| store_const   |     CheckBox |
|   store_true|        CheckBox |
|  store_False  |      CheckBox|
|       append |       TextCtrl | 
|        count| 			 DropDown|
|choice|        DropDown|




Installation instructions
------------------------  

TODO
----  

* Get this thing working. 
(picture of osx) 

* Themes 
* update graphics
* robustify parser 
* Optparse support? (do people still use it) 


Wanna help?
-----------  

Do you art? I'd love to swap out the graphics to something more stylistically unified. That ajax loader is pretty out of place.. 

Image Credits
-------------  







