import Container from '@mui/material/Container';
import Grid from '@mui/material/Unstable_Grid2';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Texts from '../components/Texts';
import ConstructionIcon from '@mui/icons-material/Construction';
import ButtonGroup from '@mui/material/ButtonGroup';
import HomeIcon from '@mui/icons-material/Home';
import UndoIcon from '@mui/icons-material/Undo';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';

export default function Tbd({setStage}) {
  const handleBack = () => setStage( e => e - 1);
  const handleHome = () => setStage( () => 0);
  return (
    <Paper elevation={5} sx={{py: 3}}>
    <Stack direction="column" spacing={2} alignItems="center">
    <Texts
      variant="h4"
      fw={500}
      text="👷 Page under Development 🚧"
    />
    <ButtonGroup variant="text" >
      <IconButton onClick={handleBack}>
          <UndoIcon/>
      </IconButton>
      <IconButton onClick={handleHome} w={9}>
          <HomeIcon/>
      </IconButton>
    </ButtonGroup>
    </Stack>
    </Paper>
  )
}

