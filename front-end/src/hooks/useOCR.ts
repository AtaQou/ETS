// import { useEffect, useRef } from "react";
// import { createWorker, Worker } from "tesseract.js";
// import html2canvas from "html2canvas";
// import { debounce } from "utils/functions";

// interface Bbox {
//   x0: number;
//   x1: number;
//   y0: number;
//   y1: number;
// }

// type Callback = (text: string, confidence: number, bbox: Bbox) => void;

// const initializeWorker = async (worker: Worker) => {
//   await worker.load();
//   await worker.loadLanguage("eng");
//   await worker.initialize("eng");
// };

// const useOCR = (callback: Callback, pageNumber: number) => {
//   const workerRef = useRef<Worker | null>(null);

//   useEffect(() => {
//     (async () => {
//       const worker = createWorker();
//       workerRef.current = await worker; // Now workerRef.current is a Worker, not a Promise<Worker>
//       if (workerRef.current) {
//         await initializeWorker(workerRef.current);
//       }
//     })();

//     return () => {
//       if (workerRef.current) {
//         workerRef.current.terminate();
//       }
//     };
//   }, []);

//   const processOCR = debounce(async () => {
//     try {
//       const pdfContainer = document.getElementById("pdf-container");
//       if (pdfContainer && workerRef.current) {
//         const canvas = await html2canvas(pdfContainer, { scale: 0.7 });
//         canvas.getContext("2d", { willReadFrequently: true });
//         console.log(canvas);

//         const {
//           data: { words },
//         } = await workerRef.current.recognize(canvas);
//         console.log({ words });
//       }
//     } catch (e) {
//       console.log(e);
//     }
//   }, 200);

//   useEffect(() => {
//     processOCR();
//   }, [processOCR]);
// };

// export default useOCR;
