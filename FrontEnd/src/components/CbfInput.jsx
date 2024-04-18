import * as React from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
export default function CbfInput({ setQuerySubmitted, setData, target }) {
  const defaultQuery =
    "I want to find books similar to Harry Potter. I like wizards and magic. Nothing too scary.";
  const [query, setQuery] = React.useState(defaultQuery);
  const [queryValid, setQueryValid] = React.useState(true);
  // form control functions
  const handleQueryChange = (e) => {
    setQueryValid(() => e.target.value.trim() !== "");
    setQuery(() => e.target.value);
  };
  const resetQuery = (e) => {
    setQueryValid(() => true);
    setQuery(() => defaultQuery);
  };
  const clearQuery = (e) => {
    setQueryValid(() => false);
    setQuery(() => "");
  };
  const handleFormSubmit = (e) => {
    e.preventDefault();
    const q = e.target.querySelector("#cbf-input").value;
    setQuerySubmitted(() => `${q}`);
  };
  return (
    <>
      <TextField
        id={target}
        label="Your Response"
        placeholder="Its empty here 😭. Populate this field with some words 😊."
        name="cbf-input"
        error={!queryValid}
        required
        multiline
        minRows={2}
        maxRows={5}
        value={query}
        autoFocus={true}
        sx={{ width: "80%" }}
        onChange={handleQueryChange}
      />
      <Stack direction="row" spacing={2} alignItems="center">
        <Button variant="contained" sx={{ px: 2 }} type="submit">
          🎉 Submit 🎉
        </Button>
        <Button variant="contained" sx={{ px: 2 }} onClick={resetQuery}>
          🔄 Reset Query 🔄
        </Button>
        <Button variant="contained" sx={{ px: 2 }} onClick={clearQuery}>
          🧹 Clear Query 🧹
        </Button>
      </Stack>
    </>
  );
}
