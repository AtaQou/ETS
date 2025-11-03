import { useState, useEffect, useContext } from "react";
import axios from "axios";
import { Context } from "../context/Context";
import { FaRegSquare, FaCheckSquare } from "react-icons/fa";
import { RiDeleteBin4Fill } from "react-icons/ri";
import { apiURL } from "../utils/consts";
import { getBgSecondary, getFontColorSecondary } from "../utils/functions";
import React from "react";
import Button from "./ui/Button";
import { Document, IContextProps, ID } from "types/AppTypes";
import Dialog from "./ui/Dialog";

interface DocumentsProps {
  docID:ID;
  setDocID: React.Dispatch<React.SetStateAction<ID>>;
  onConfirm: (id: ID) => void;
}

const Documents: React.FC<DocumentsProps> = ({ docID, setDocID, onConfirm }) => {
  const [documents, setDocuments] = useState<Document[]>();
  const [loading, setLoading] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [error, setError] = useState(null);
  const { userInfo, selectedDocID, setSelectedDocID, userSettingsApi } = useContext<IContextProps>(Context);
  

  const { userID } = userInfo;
  const isDarkTheme = userSettingsApi.theme === "dark";

  const handleDocumentClick = (docId: ID) => {
    if (docId === docID) {
      setDocID("");
    } else {
      setDocID(docId);
    }
  };

  const onDoubleClick = (id: ID) => {
    setDocID(id);
    onConfirm(id);
  };

  const onClickDelete = (id: ID) => {
    setSelectedDocID?.(id);
    setShowDeleteDialog(true);
  };

  const onDialogClose = () => {
    setShowDeleteDialog(false);
  };

  const onDialogConfirm = () => {
    axios
      .delete(`${apiURL}/delete_file`, {
        params: {
          userID,
          docID: selectedDocID,
        },
      })
      .then((response) => {
        setShowDeleteDialog(false);
        setDocuments((prev) => {
          return prev?.filter((doc) => doc.docID !== selectedDocID);
        });
        setSelectedDocID?.("");
        alert("File successfully deleted");
      })
      .catch((err) => {
        setShowDeleteDialog(false);
      });
  };

  useEffect(() => {
    setLoading(true);
    axios
      .get(`${apiURL}/documents`, {
        params: {
          userID,
        },
      })
      .then((response) => {
        setDocuments(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [userID]);

  if (loading) {
    return <div className='flex justify-center items-center w-full h-full'>Loading documents...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <>
      {showDeleteDialog && (
        <Dialog
          title='Delete'
          content='Are you sure you want to delete this document?'
          onClose={onDialogClose}
          onConfirm={onDialogConfirm}
        />
      )}
      <div
        className='mb-4'
        style={{
          backgroundColor: getBgSecondary(isDarkTheme),
        }}
      >
        <div
          id='header'
          className={`grid grid-cols-7 text-left border-b-2 sticky top-0 pl-10 pt-2 border-slate-100 w-full`}
          style={{
            color: getFontColorSecondary(isDarkTheme),
            backgroundColor: getBgSecondary(isDarkTheme),
          }}
        >
          <div className='py-2 col-span-3 font-bold'>Document name</div>
          <div className='py-2 col-span-1 font-bold'>Last read page</div>
          <div className='py-2 col-span-2 font-bold'>Upload date</div>
          <div className='py-2 px-1 col-span-1 font-bold ml-[-15px]'>Actions</div>
        </div>
        {documents?.map((doc) => (
          <div className='flex items-center px-4' style={{ color: getFontColorSecondary(isDarkTheme) }}>
            <div
              onClick={() => handleDocumentClick(doc.docID)}
              className='flex items-center justify-center h-6 w-6  cursor-pointer m-1'
              style={{ color: getFontColorSecondary(isDarkTheme) }}
            >
              {docID === doc.docID ? <FaCheckSquare /> : <FaRegSquare />}
            </div>
            <div
              key={doc.docID}
              className={`grid grid-cols-7 text-left border-b-2 border-slate-100 top-0 hover:bg-[${getBgSecondary(
                isDarkTheme
              )}] transition-colors duration-200 text-sm w-full bg-[${
                docID === doc.docID ? `${getBgSecondary(isDarkTheme)}` : ""
              }]`}
              onDoubleClick={() => onDoubleClick(doc.docID)}
            >
              <div className='flex items-center px-1 py-2 col-span-3 xl:w-80 lg:w-36 truncate'>{doc.docName}</div>
              <div className='flex items-center px-1 py-2 col-span-1'>{doc.lastReadPage}</div>
              <div className='flex items-center px-1 py-2 col-span-2'>{doc.uploadDate.split(".")[0]}</div>
              <div className='flex items-center py-2 col-span-1'>
                <Button className='p-0' onClick={() => onClickDelete(doc.docID)}>
                  <RiDeleteBin4Fill className='text-[1.1rem] text-red-700 hover:text-red-600' />
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>
  );
};

export default Documents;
