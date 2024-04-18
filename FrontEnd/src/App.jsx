import * as React from "react";
import Container from "@mui/material/Container";
import Header from "./sections/Header";
import Landing from "./sections/Landing";
import Choose from "./sections/Choose";
import Tbd from "./sections/Tbd";
import Cbf from "./sections/Cbf";
import Cf from "./sections/Cf";

export default function App() {
  const [stage, setStage] = React.useState(0);
  const [mode, setMode] = React.useState(0);

  return (
    <Container maxWidth="md">
      <Header setStage={setStage} />
      {stage === 0 ? <Landing setStage={setStage} /> : <></>}
      {stage === 1 ? <Choose setStage={setStage} setMode={setMode} /> : <></>}
      {stage === 2 && mode == 0 ? <Cbf setStage={setStage} /> : <></>}
      {stage === 2 && mode == 1 ? <Cf setStage={setStage} /> : <></>}
    </Container>
  );
}
