import "./PlateDetectionView.css";
import { Button } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import { useState, useEffect } from "react";
import axios from "axios";
import { AllowedPlatesList } from "./AllowedPlatesList";
import { DetectedPlatesList } from "./DetectedPlatesList";
import image from "../../images/placeholder.jpg"

const url = "http://license-plates-api.westeurope.azurecontainer.io/";
const tmpPlates = [
  "XS 55 032",
  "FA 22 911",
  "ERA 81TL",
  "DW 688CC",
  "XS 55 012",
  "FA 22 921",
  "ERA 811L",
  "DW 6811C",
  "XS 55 122",
  "FA 22 sa1",
  "ERA 822L",
  "DW 633CC",
  "XS 55 0qq",
  "FA 22 fs1",
  "ERA 118 TL",
  "DW 681 12",
];

export function PlateDetectionView() {
  const [isFetching, setIsFetching] = useState(false);
  const [allowedPlates, setAllowedPlates] = useState([]);
  const [videoFile, setVideoFile] = useState(null);
  const [detectedPlates, setDetectedPlates] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(url + "license-plates");

      console.log(result);
      setAllowedPlates(result.data);
    };

    fetchData();
    setAllowedPlates(tmpPlates);
  }, []);

  const sendVideo = () => {
    setIsFetching(true);
    var formData = new FormData();
    formData.append("uploaded_file ", videoFile);
    axios.post(url+'detections', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    ).then(response => setDetectedPlates(response.data));
    const tmpDetected = ["FA 22 911", "ERA 81TL"]
    console.log(tmpDetected)
    setDetectedPlates(tmpDetected)
    setIsFetching(false);
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
        <Button className="analize_button" component="span" disabled={videoFile ? false : true} onClick={(e) => sendVideo()} variant="contained">
            Analize video
        </Button>
      </div>
      
      <div className="uploaded-video">
        {videoFile ? (
          <video key={videoFile.name} width="500" height="281" controls>
            <source src={URL.createObjectURL(videoFile)} />
          </video>
        ) :
        <img width="500" src={image} alt="placeholder" /> 
      }
      </div>
      <div className="detected-plates">
         
        <DetectedPlatesList list={detectedPlates} isFetching={isFetching}/>
        
      </div>
     
    </div>
    </>
  );
}
