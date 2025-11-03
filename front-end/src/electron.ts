// import { app, BrowserWindow } from "electron";
// import * as path from "path";
// import * as isDev from "electron-is-dev";

// let mainWindow: BrowserWindow | null = null;

// const createWindow = (): void => {
//   mainWindow = new BrowserWindow({
//     width: 900,
//     height: 680,
//     webPreferences: {
//       nodeIntegration: true,
//     },
//   });

//   // mainWindow.setMenuBarVisibility(false);

//   const startUrl = isDev
//     ? "http://localhost:3000"
//     : `file://${path.join(__dirname, "../build/index.html")}`;
//   mainWindow.loadURL(startUrl);
//   mainWindow.on("closed", () => {
//     mainWindow = null;
//   });
// };

// app.on("ready", createWindow);

// app.on("window-all-closed", () => {
//   if (process.platform !== "darwin") {
//     app.quit();
//   }
// });

// app.on("activate", () => {
//   if (mainWindow === null) {
//     createWindow();
//   }
// });
