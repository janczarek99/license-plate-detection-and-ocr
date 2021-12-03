import * as React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

export function AllowedPlatesList(props) {
  console.log(props.list);

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
        Allowed plates:
      </Typography>
      {props.list ? (
        <List
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
              <ListItemText primary={item} />
            </ListItem>
          ))}
        </List>
      ) : (
        <Box
          sx={{
            position: "absolute",
            marginTop: "50px",
            marginLeft: "50px",
          }}
        >
          <CircularProgress size="50px" />
        </Box>
      )}
    </div>
  );
}
