# Using Gooey as a frontend for any language. 

Gooey can be used as the frontend for _any_ language. Whether you've built your application in Java, Node, or Haskell, Gooey can still be used to create a fast, free UI with just a little bit of Python.  




Gooey let's you specify the `target` that is should execute during runtime as an argument to the main decorator.

 

Clojure example: 

```
lein new app clojure-program
```


```
(ns clojure-program.core
  (:gen-class))

(defn -main
  "Tiny example."
  [& args]
  (println "here are the args: " args)
  (doseq [x (range 10)]
    (println x)
    (Thread/sleep 500)))    
```

```
lein uberjar
```

```
./target/uberjar/clojure-program-0.1.0-SNAPSHOT-standalone.jar
```

```
java -jar target/uberjar/clojure-program-0.1.0-SNAPSHOT-standalone.jar -arg1 foo -arg2 bar
```

```
here are the args:  (-f foo -b qwer)
0
1
2
3
etc...
```




```
mkdir clojure-ui-example 
cd clojure-ui-example 
```

```
virtualenv venv
pip install gooey
```

```
mkdir resources
```


src/main.py
```
from gooey import Gooey, GooeyParser, local_resource_path


jar_path = local_resource_path('resources/clojure-gooey-0.1.0-SNAPSHOT-standalone.jar')

@Gooey(image_dir=local_resource_path('stuff/images/'), target='java -jar ' + jar_path)
def main():
    parser = GooeyParser(description="My program")
    parser.add_argument('filename', metavar='Filename', help='filename', widget='FileChooser')
    parser.parse_args()


if __name__ == '__main__':
    main()
```





