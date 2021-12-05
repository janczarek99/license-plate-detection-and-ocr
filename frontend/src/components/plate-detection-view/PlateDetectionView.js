import "./PlateDetectionView.css";
import { Button } from "@mui/material";
import { useState, useEffect } from "react";
import axios from "axios";
import { AllowedPlatesList } from "./AllowedPlatesList";
import { DetectedPlatesList } from "./DetectedPlatesList";
import image from "../../images/placeholder.jpg";
import Alert from '@mui/material/Alert';

const url = "https://license-plates-api-proxy.westeurope.cloudapp.azure.com/";

export function PlateDetectionView() {
  const [isFetching, setIsFetching] = useState(false);
  const [allowedPlates, setAllowedPlates] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [detectedPlates, setDetectedPlates] = useState(null);
  const [access, setAccess] = useState([""]);
  const [notFoundPlates, setNotFoundPlates] = useState(false);
  const [videoTooLong, setVideoTooLong] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");


  console.log("v47");
  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(url + "license-plates");
      const tmpAllowedPlates = {"data": ['WF80350', 'SBI91126', 'PZ825UA', 'WN2845M', 'WPI1694G', 'CSWVE20']};
      setAllowedPlates(tmpAllowedPlates); //mock for testing purposes
      console.log(allowedPlates)
    };

    fetchData();
  }, []);

  const sendVideo = async () => {
    setIsFetching(true);
    var formdata = new FormData();
    formdata.append("uploaded_file", videoFile, "[PROXY]");

    var requestOptions = {
      method: "POST",
      body: formdata,
      redirect: "follow",
    };

    await fetch(
      url+"detections",
      requestOptions
    )
    .then(response => response.json())
    .then(result => {console.log(result); setNotFoundPlates(false); setVideoTooLong(false);  if(result.detail){setVideoTooLong(true); setErrorMsg(result.detail.detail);} else if(result.data.length ==0){setNotFoundPlates(true);} setDetectedPlates(result.data); setAccess(['CSWVE20'])})
    .catch((error) => {setIsFetching(false); console.log(error);});

    setIsFetching(false);
  };

  const checkAccess = (detected, allowed)=> {
    if (detected && allowed){
      var accessL=getArraysIntersection(detected, allowed);
    setAccess(accessL);
    }
  }

  const getArraysIntersection = (array1, array2) =>{
    var intersection = array1.filter(function(x) {
      if(array2.indexOf(x) !=- 1)
        return true;
      else
        return false;
    });
    var filtered_intersection = [...new Set(intersection)];
    return filtered_intersection;
  }

  return (
    <>
      <div className="title">
        <h1>Plate Detector</h1>
      </div>
      <div className="center-screen">
        <AllowedPlatesList list={allowedPlates} />
        <div className="upload-button">
          <input
            accept="video/mp4,video/x-m4v,video/*"
            className="input"
            style={{ display: "none" }}
            id="contained-button-file"
            type="file"
            onChange={(e) => {
              console.log(e.target.files[0]);
              setVideoFile(null);
              setVideoFile(e.target.files[0]);
            }}
          />
          <label htmlFor="contained-button-file">
            <Button variant="outlined" component="span" className="button">
              Upload
            </Button>
          </label>
        </div>
        <div className="send-button">
          <Button
            className="analize_button"
            component="span"
            disabled={videoFile ? false : true}
            onClick={(e) => sendVideo()}
            variant="contained"
          >
            Analize video
          </Button>
        </div>

        <div className="uploaded-video">
          {videoFile ? (
            <video key={videoFile.name} width="500" height="281" controls>
              <source src={URL.createObjectURL(videoFile)} />
            </video>
          ) : (
            <img width="500" src={image} alt="placeholder" />
          )}
        </div>
        <div className="detected-plates">
          <DetectedPlatesList list={detectedPlates} accessList={access} isFetching={isFetching} />
        </div>
        <div className="alert">
          {notFoundPlates && <Alert severity="info" onClose={() => {setNotFoundPlates(false)}}>No plates found!</Alert>}
          {videoTooLong && <Alert severity="error" onClose={() => {setVideoTooLong(false)}}>{errorMsg}</Alert>}
        </div>
      </div>
    </>
  );
}
