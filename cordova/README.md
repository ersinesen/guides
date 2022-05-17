# Reactjs web app to mobile app conversion with Cordova

1. Install cordova
```
npm i -g cordova
```

2. Create cordova project at project root dir
``` 
cordova create cordova
```

3. Modify package.json
```
// ...
"private": true,
"homepage": "./",
"dependencies": {
// ...

```
4. Move ./cordova/www/js/index.js to ./public

5. Update ./public/index.html
```
div id="root"></div>
    <!-- this is your cordova script index.js file: -->
    <script src="index.js"></script>
```

6. Update src/index.tsx, after imports
```
declare global {
  interface Window { cordova: any; }
}

window.cordova = window.cordova || false;
```

7. Update build command in package.json
```
    "build": "react-scripts build && cp -r build/* ./cordova/www",
```

8. Build project
```
npm run build
```

9. Go to cordova directory and build for desired platform
```
cd cordova
cordova platform add android
cordova build android
```

# Cordova Commands

```
cordova clean
cordova platform remove android
cordova platform add android
cordova build android
cordova build --release android
cordova build android --release -- --keystore=~/Documents/x.jks --storePassword=x --alias=x --password=x --packageType=bundle

```


# Links

[Turning Reactjs to Mobile App with Cordova ](https://fjolt.com/article/react-apache-cordova-ios-android)

[Android App Signing](https://developer.android.com/studio/publish/app-signing.html)