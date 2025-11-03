import "react-pdf/dist/esm/Page/TextLayer.css";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { pdfjs, Document, Page } from "react-pdf";
import { StyleSheet } from "@react-pdf/renderer";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import { useSnackbar } from "../hooks/useSnackbar";
import { debounce } from "../utils/functions";
import { Context } from "../context/Context";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/legacy/build/pdf.worker.min.js`;

interface LoadSuccessParams {
  numPages: number;
  getPage: (pageNumber: number) => Promise<any>;
}

const styles = StyleSheet.create({
  page: {
    flexDirection: "row",
  },
});

const FileViewer: React.FC = () => {
  const {
    file,
    setLoading,
    setCurrentPage,
    pageCount,
    setScrollTop,
    userSettingsApi,
    setPageCount,
    pdfDimensions,
    setPdfDimensions,
    setPageMounted,
  } = useContext(Context);
  const isElectron = /Electron/.test(navigator.userAgent);
  const [elWidth, setElWidth] = useState<number>();
  const { triggerSnackbar } = useSnackbar();
  const { zoom: savedZoom } = userSettingsApi;

  const wrapperStyle = useMemo(
    () => ({
      width: "100%",
      height: `calc(100vw / ${pdfDimensions.aspectRatio})`,
      maxHeight: isElectron ? "89.1vh" : "91%",
    }),
    [isElectron, pdfDimensions.aspectRatio]
  );

  const onDocumentLoadSuccess = async (pdf: LoadSuccessParams) => {
    console.log("doc load success");
    setPageCount?.(pdf.numPages);
    setLoading?.(false);
    setTimeout(() => {
      setPageMounted?.();
      // Wait for the canvas to render because the width is (2) not correct for a split second
    }, 200);
    triggerSnackbar({
      message: "Document loaded successfully!",
      status: "success",
      open: true,
    });
    // Get the first page of the document
    const page = await pdf.getPage(1);

    // Wait for the next tick to ensure the DOM is updated
    setTimeout(() => {
      const element = document.querySelector(".react-pdf__Page");
      if (element) {
        const rect = element.getBoundingClientRect();
        const width = rect.width;
        const height = rect.height;

        const aspectRatio = width / height;
        setPdfDimensions?.({ aspectRatio, width, height: height + 34 });
      }
    }, 500);

    page.cleanup();
  };

  const handleScroll = useCallback(
    (event: React.UIEvent<HTMLDivElement>) => {
      event.stopPropagation();
      event.preventDefault();

      const container = event.target as HTMLDivElement;
      const pageHeight = pdfDimensions.height;

      const scrolledPages =
        Math.floor((container.scrollTop + pageHeight / 4) / pageHeight) + 1;
      const containerElement = document.getElementById("pdf-container");
      if (containerElement) setScrollTop?.(containerElement?.scrollTop);
      setCurrentPage?.(scrolledPages);
    },
    [pdfDimensions.height, setCurrentPage, setScrollTop]
  );

  // const debouncedScroll = debounce(handleScroll, 250);

  useEffect(() => {
    const containerElement = document.getElementById("pdf-container");
    const { width = 0 } = containerElement
      ? containerElement.getBoundingClientRect()
      : {};
    setElWidth(width);
  }, []);

  useEffect(() => {
    const updatePdfDimensions = () => {
      setTimeout(() => {
        const element = document.querySelector(".react-pdf__Page");
        if (element) {
          const rect = element.getBoundingClientRect();
          const width = rect.width;
          const height = rect.height;

          const aspectRatio = width / height;
          setPdfDimensions?.({ aspectRatio, width, height: height + 34 });
        }
      }, 500);
    };

    const debouncedUpdatePdfDimensions = debounce(updatePdfDimensions, 500);
    window.addEventListener("resize", debouncedUpdatePdfDimensions);

    return () => {
      window.removeEventListener("resize", debouncedUpdatePdfDimensions);
    };
  }, [setPdfDimensions]);

  return (
    <div
      className={`${
        savedZoom >= 1 ? "justify-start" : "justify-center"
      } flex overflow-auto lg:h-[88%]`}
      id='pdf-container'
      style={{ ...wrapperStyle, scrollBehavior: "smooth" }}
      onScroll={handleScroll}
    >
      <Document
        file={file instanceof Blob ? file : undefined}
        onLoadSuccess={onDocumentLoadSuccess}
        loading=''
      >
        {Array.from(new Array(pageCount), (el, index) => (
          <div
            id='pdf-page'
            key={`wrapper_${index}`}
            style={{ height: pdfDimensions.height, ...styles.page }}
            data-page-number={index}
          >
            <Page
              loading=''
              className='mb-8 border border-gray-300'
              key={`page_${index + 1}`}
              pageNumber={index + 1}
              scale={savedZoom}
              renderMode='canvas'
              renderTextLayer={false}
              width={elWidth}
            />
          </div>
        ))}
      </Document>
    </div>
  );
};

export default FileViewer;
