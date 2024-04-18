import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import Texts from "../components/Texts";

export default function Landing({ setStage }) {
  return (
    <Paper elevation={5} sx={{ my: 4 }}>
      <Grid
        container
        spacing={{ xs: 2, sm: 4, md: 6 }}
        p={2}
        justifyContent="center"
      >
        <Stack direction="row">
          <Grid xs={7} sm={6} md={7}>
            <Stack
              alignItems="center"
              justifyContent="space-around"
              spacing={{ xs: 1, sm: 8, md: 10 }}
              direction="column"
            >
              <Stack alignItems="center" spacing={{ xs: 1, sm: 4, md: 6 }}>
                <Texts variant="h3" text="Explore..." fw="700" />
                <Texts
                  variant="h5"
                  text="the vast world of books 📚"
                  fw="500"
                />
                <Texts
                  variant="h6"
                  text="... through personalized recommendations 😊"
                  fw="300"
                />
              </Stack>
              <Button
                variant="contained"
                onClick={() => setStage((e) => e + 1)}
              >
                🚀 Get Started!
              </Button>
            </Stack>
          </Grid>
          <Grid xs={5} sm={6} md={5}>
            <img
              src="landing.jpg"
              style={{
                maxWidth: "100%",
                maxHeight: "100vh",
                border: "5px solid silver",
              }}
            />
          </Grid>
        </Stack>
      </Grid>
    </Paper>
  );
}
