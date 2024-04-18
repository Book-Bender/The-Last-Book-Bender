import Typography from "@mui/material/Typography";

export default function Texts({ variant, text, fw }) {
  return (
    <Typography
      variant={variant}
      textAlign="center"
      fontWeight={fw ? fw : "300"}
    >
      {text}
    </Typography>
  );
}
