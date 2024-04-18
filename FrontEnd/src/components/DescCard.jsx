import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import Texts from "../components/Texts";
import Card from "@mui/material/Card";
import Box from "@mui/material/Box";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import CardMedia from "@mui/material/CardMedia";

export default function DescCard({ txtobj, imgobj, onClick }) {
  const { title, subtitle, btntxt } = txtobj;
  const { fname, alt } = imgobj;
  return (
    <Box mb={3} sx={{ alignItems: "center" }}>
      <Card sx={{ p: 6 }} elevation={6}>
        <Stack spacing={1} alignItems="center">
          <CardMedia
            component="img"
            image={`/${fname}`}
            width="80%"
            alt={alt}
            sx={{ border: "4px silver solid" }}
          ></CardMedia>
          <CardContent>
            <Texts text={title} variant="h6" fw="500" />
          </CardContent>
          <CardActions>
            <Button variant="contained" sx={{ px: 2 }} onClick={onClick}>
              {btntxt}
            </Button>
          </CardActions>
        </Stack>
      </Card>
    </Box>
  );
}
