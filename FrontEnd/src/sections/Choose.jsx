import Container from '@mui/material/Container';
import Grid from '@mui/material/Unstable_Grid2';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Texts from '../components/Texts';
import DescCard from '../components/DescCard';

export default function Choose({setStage, setMode}) {
  const handleClick = () => setStage( e => e + 1);
  return (
    <Paper elevation={3} sx={{p: 2}}>
      <Stack direction="column" spacing={2}>
        <Texts
          variant="h3"
          fw="500"
          text="Tell us your preference."
        />
        <Texts
          variant="h4"
          fw="300"
          text="Choose from a method below."
        />
        <Grid container spacing={1} justifyContent="space-around">
          <Grid xs={5}>
            <DescCard
              txtobj={
                {
                  title: "Tell us your interest by entering a prompt.",
                  btntxt: "Choose CBF"
                }
              }
              imgobj={
                {
                  alt: "CBF (Content-Based Filtering) Diagram",
                  fname: "cbf.png"
                }
              }
              onClick={
                () => {
                  setMode(() => 0)
                  setStage(x => x + 1)
                }
              }
            />
          </Grid>
          <Grid xs={5}>
            <DescCard
              txtobj={
                {
                  title: "Tell us your interest by finding a similar user",
                  btntxt: "Choose CF"
                }
              }
              imgobj={
                {
                  alt: "CF (Collaborative Filtering) Diagram",
                  fname: "cf.png"
                }
              }
              onClick={
                () => {
                  setMode(() => 1)
                  setStage(x => x + 1)
                }
              }
            />
          </Grid>
        </Grid>
      </Stack>
    </Paper>
  )
}
