import * as React from "react";

import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Chip from "@mui/material/Chip";
import Pagination from "@mui/material/Pagination";

import axios from "axios";

import Texts from "../components/Texts";
import DescCard from "../components/DescCard";
import SmallNav from "../components/SmallNav";
import Lister from "../components/Lister";
import ForceGraph from "../components/ForceGraph";
import CbfInput from "../components/CbfInput";
import FaceIcon from "@mui/icons-material/Face";

const extractratings = (data, userids, userfocused) =>
  data.filter((e) => userids[userfocused] === e.u);

export default function RatingsView({ data, userIds, userFocused }) {
  const ratings = extractRatings(data, userIds, userFocused);
  return (
    <Paper sx={{ overflow: "hidden", p: 1 }} elevation={1}>
      <Stack direction="column" alignItems="center">
        <Grid column="true">{ratings[0].b}</Grid>
      </Stack>
    </Paper>
  );
}
