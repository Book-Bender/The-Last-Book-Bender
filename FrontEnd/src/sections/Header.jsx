import GitHubIcon from '@mui/icons-material/GitHub';
import Grid from '@mui/material/Unstable_Grid2';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import Tooltip from '@mui/material/Tooltip';
import Button from '@mui/material/Button';

const RepoIcon = () => {
  return ( 
    <Tooltip title="Link to Our Repo" placement="left">
      <IconButton>
        <Link
          href="https://github.com/Book-Bender/The-Last-Book-Bender"
          target="_blank"
        >
          <GitHubIcon/>
        </Link>
      </IconButton>
    </Tooltip>
  )
}

const Title = ({onClick}) => {
  return (
    <Tooltip title="CSE6242 - Demo App" placement="right">
      <Button color="primary" onClick={onClick}>
        The Last Book Bender
      </Button>
    </Tooltip>
  )
}

export default function Header({setStage}) {
  const handleClick = () => setStage(() => 0)
  return (
      <Paper elevation={0} sx={{ my: 1 }}>
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          spacing={0}
          sx={{px: 1}}
        >
          <Title onClick={handleClick}/>
          <RepoIcon/>
        </Stack>
      </Paper>
  );
}

