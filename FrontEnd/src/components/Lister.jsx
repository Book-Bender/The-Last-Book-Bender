import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";

export default function Lister({ data }) {
  return (
    <List>
      {data.length === 0 ? (
        <></>
      ) : (
        data.map((r, _) => <ListItem key={_}>{r.title}</ListItem>)
      )}
    </List>
  );
}
