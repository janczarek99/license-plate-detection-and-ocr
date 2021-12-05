import * as React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

export function DetectedPlatesList(props) {

  console.log(props.accessList)

  const text = {
    color: "#006600"
};

  return (
    <div>
      <Typography
        sx={{
          mt: 4,
          mb: 2,
          fontSize: "20px",
          backgroundColor: "#1976d2",
          color: "#ffffff",
          borderRadius: "5px",
          padding: "10px",
        }}
        variant="h6"
        component="div"
      >
        Detected plates:
      </Typography>
      {props.isFetching ? 
        <Box
          sx={{
            position: "absolute",
            marginTop: "50px",
            marginLeft: "50px",
          }}
        >
          <CircularProgress size="50px" />
        </Box>
       : 
          props.list && <List
            sx={{
              width: "100%",
              maxWidth: 360,
              bgcolor: "background.paper",
              position: "relative",
              overflow: "auto",
              maxHeight: 300,
              "& ul": { padding: 0 },
            }}
          >
            {props.list.map((item, index) => (
              <ListItem key={`allowed-plate-${index}`}>
              {props.accessList.includes(item) ? (<ListItemText primaryTypographyProps={{ style: text }} primary={item} />) : (<ListItemText primary={item} />)}
                
              </ListItem>
            ))}
          </List>
      }
    </div>
  );
}
