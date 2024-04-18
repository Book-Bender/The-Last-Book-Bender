import * as React from "react";

import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";

import axios from "axios";

import Texts from "../components/Texts";
import DescCard from "../components/DescCard";
import SmallNav from "../components/SmallNav";
import Lister from "../components/Lister";
import ForceGraph from "../components/ForceGraph";
import CbfInput from "../components/CbfInput";

const meltJson = (e) => {
  return Object.entries(e)
    .map((r) => r[1])
    .sort((r1, r2) => r1.score - r2.score);
};

export default function Cbf({ setStage }) {
  const defaultQuery =
    "I want to find books similar to Harry Potter. I like wizards and magic. Nothing too scary.";
  // const [query, setQuery] = React.useState(defaultQuery);
  // const [queryValid, setQueryValid] = React.useState(true);
  const [querySubmitted, setQuerySubmitted] = React.useState("");
  const [data, setData] = React.useState([]);

  const fetchData = async (q) => {
    const res = await axios.get(`http://127.0.0.1:5000/api/cbf/${q}`);
    setData(() => meltJson(res.data));
  };

  React.useEffect(() => {
    querySubmitted.trim() !== "" ? fetchData(querySubmitted) : "";
  }, [querySubmitted]);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const q = e.target.querySelector("#cbf-input").value;
    q.trim() !== "" ? setQuerySubmitted(() => `${q}`) : null;
  };
  return (
    <Paper elevation={5} sx={{ p: 2 }}>
      <form noValidate onSubmit={handleFormSubmit}>
        <Stack direction="column" spacing={1} alignItems="center">
          <label htmlFor="cbf-input">
            <Texts variant="h5" fw="300" text="Describe your book interests." />
          </label>
          <SmallNav setStage={setStage} />
          <CbfInput
            setQuerySubmitted={setQuerySubmitted}
            setData={setData}
            target="cbf-input"
          />
          {data.length === 0 ? (
            <></>
          ) : (
            <ForceGraph
              querySubmitted={querySubmitted}
              data={data}
              mode="cbf"
              key={querySubmitted}
            />
          )}
        </Stack>
      </form>
    </Paper>
  );
}
