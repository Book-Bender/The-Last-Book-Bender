import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import Texts from "../components/Texts";
import ConstructionIcon from "@mui/icons-material/Construction";
import ButtonGroup from "@mui/material/ButtonGroup";
import HomeIcon from "@mui/icons-material/Home";
import UndoIcon from "@mui/icons-material/Undo";
import Tooltip from "@mui/material/Tooltip";

export default function SmallNav({ setStage }) {
  const handleBack = () => setStage((e) => e - 1);
  const handleHome = () => setStage(() => 0);
  return (
    <ButtonGroup variant="text">
      <Tooltip title="To Previous Page" placement="left">
        <IconButton onClick={handleBack}>
          <UndoIcon />
        </IconButton>
      </Tooltip>
      <Tooltip title="Back to Home" placement="right">
        <IconButton onClick={handleHome} w={9}>
          <HomeIcon />
        </IconButton>
      </Tooltip>
    </ButtonGroup>
  );
}
