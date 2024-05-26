import * as React from "react";

import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Chip from "@mui/material/Chip";
import Rating from "@mui/material/Rating";
import Pagination from "@mui/material/Pagination";
import FaceIcon from "@mui/icons-material/Face";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";

import axios from "axios";

import Texts from "../components/Texts";
import DescCard from "../components/DescCard";
import SmallNav from "../components/SmallNav";
import Lister from "../components/Lister";
import ForceGraph from "../components/ForceGraph";
import CbfInput from "../components/CbfInput";
// import RatingsView from "../components/RatingsView";

const getUserIds = (data) => {
  if (data) {return [...new Set(data.map((e) => e.u))]}
  else {return []}
}
const extractRatings = (data, userids, userfocused) =>
  data.filter((e) => userids[userfocused] === e.u);

const meltJson = (e) => {
  return Object.entries(e)
    .map((r) => r[1])
    .sort((r1, r2) => r1.score - r2.score);
};

function RatingsView({ data, userIds, userFocused }) {
  const ratings = extractRatings(data, userIds, userFocused);
  const [page, setPage] = React.useState(0);
  React.useEffect(() => setPage(() => 0), [userFocused, userIds]);
  return (
    <Paper sx={{ overflow: "hidden", p: 1 }} elevation={1}>
      <Stack direction="column" alignItems="center">
        <Grid column="true">
          <Typography
            variant="subtitle1"
            display="block"
            gutterBottom
            px={4}
            sx={{ textAlign: "center", fontStyle: "italic" }}
          >
            {ratings[page].b}
          </Typography>
        </Grid>
        <Rating
          value={+ratings[page].r}
          readOnly
          icon={<FavoriteIcon fontSize="inherit" />}
          emptyIcon={<FavoriteBorderIcon fontSize="inherit" />}
          sx={{ mb: 1.5 }}
        />
        <Pagination
          defaultPage={1}
          page={page + 1}
          count={ratings.length}
          color="primary"
          onChange={(e, n) => setPage(() => n - 1)}
          mt={1}
        />
      </Stack>
    </Paper>
  );
}

export default function Cf({ setStage }) {
  const [refresh, setRefresh] = React.useState(0);
  const [userFocused, setUserFocused] = React.useState(0);
  // const [query, setQuery] = React.useState(defaultQuery);
  // const [queryValid, setQueryValid] = React.useState(true);
  const [querySubmitted, setQuerySubmitted] = React.useState("");
  const [data, setData] = React.useState([]);
  const [recData, setRecData] = React.useState([]);

  const fetchData = async () => {
    const res = await axios.get(`http://127.0.0.1:5000/api/sample_users`);
    setData(() => res.data.result);
  };

  React.useEffect(() => {
    // setData(() => []);
    setUserFocused(() => 0);
    fetchData();
  }, [refresh]);

  const userIds = getUserIds(data);

  // handle clicking on user buttons
  const handleSwitchUser = (e) => () => setUserFocused(e);
  const handleReroll = () => setRefresh(e => e + 1)
  const handleSubmit = () => setQuerySubmitted(() => userIds[userFocused])

  const fetchRecData = async (q) => {
    const res = await axios.get(`http://127.0.0.1:5000/api/cf/${q}`);
    setRecData(() => meltJson(res.data));
  };

  React.useEffect(
    () => {
      if (querySubmitted.length > 0) {
        fetchRecData(querySubmitted)
      }
    },
    [querySubmitted]
  )

  return (
    <Paper elevation={5} sx={{ p: 2 }}>
      <Stack alignItems="center">
        <Texts
          variant="h5"
          fw="300"
          text="Let us help you find a similar user."
        />
        <SmallNav setStage={setStage} />
        {data.length === 0 ? (
          <></>
        ) : (
          <Grid container spacing={3} my={2} px={2}>
            <Grid container xs={5} spacing={1}>
              <Grid xs={12}>
                <Texts variant="body1" fw="700" text="Sampled User IDs." />
              </Grid>
              {[...new Array(userIds.length).keys()].map((e) => (
                <Grid xs={4} mt={2} key={userIds[e]} item="true">
                  <Button
                    variant={e === userFocused ? "contained" : "outlined"}
                    size="medium"
                    key={userIds[e]}
                    startIcon={<FaceIcon />}
                    onClick={handleSwitchUser(e)}
                  >
                    {userIds[e].padStart(5, "0")}
                  </Button>
                </Grid>
              ))}
            </Grid>
            <Grid container xs={7}>
              <Grid xs={12}>
                <RatingsView
                  userIds={userIds}
                  data={data}
                  userFocused={userFocused}
                />
              </Grid>
              <Grid xs={12}>
              <Stack direction="row" spacing={2} alignItems="center" justifyContent="center">
                <Button variant="contained" sx={{ px: 2 }} onClick={handleReroll}>
                  🎲 Reroll Users 🎲
                </Button>
                <Button variant="contained" sx={{ px: 2 }} onClick={handleSubmit}>
                  ✅ Select this User ✅
                </Button>
              </Stack>
              </Grid>
            </Grid>
          </Grid>
        )}
          {recData.length === 0 ? (
            <></>
          ) : (
            <ForceGraph
              querySubmitted={querySubmitted}
              data={recData}
              mode="cf"
              key={querySubmitted}
            />
          )}
      </Stack>
    </Paper>
  );
}
