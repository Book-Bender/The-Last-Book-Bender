function recommendBooks() {
    let element = document.getElementById("force_graph");

    if (element != null) {
        element.remove();
    }

    let query = document.getElementById("user_query");

    if (query.value === '') {
        alert("Please enter some text before querying!")
    }
    else {
        const url = `http://localhost:5000/recommend/${query.value}`
        fetch(url)
            .then(response => response.json())
            .then(json => {
                json['query'] = {
                    'score': 0,
                    'title': query.value,
                    'pandas_index': -1,
                }
                generate_force_graph(json);
            })
    }
}

function generate_force_graph(recommendations) {
    let links = [];
    let nodes = {};
    let width = window.innerWidth, height = 800;

    // compute the distinct nodes from the links.
    for (let key in recommendations) {
        links.push({
            "source": nodes['query'] || (nodes['query'] = {name: recommendations['query'].title, pandas_index: -1}),
            "target": nodes[key] || (nodes[key] = {name: recommendations[key].title, pandas_index: recommendations[key].pandas_index}),
            "distance": recommendations[key].score
        })
    }

    let force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(function(link) {
            return 2 ** link.distance;
        }))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-300).distanceMax(100))
        .alphaTarget(1)
        .on("tick", tick);

    let svg = d3.select("body").append("svg")
        .attr("id", "force_graph")
        .attr("width", width)
        .attr("height", height);

    // add the links
    let path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("id", function(d) { return d.value == 0 ? "similar" : "not-similar"; })
        .attr("class", function(d) { return "link " + d.type; });

    // define the nodes
    let node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", function(d) {
            if (d.index == Object.keys(recommendations).length - 1) {
                return "query node";
            }
            return `node-${d.pandas_index}`;
        })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

    // add the nodes
    node.append("circle")
        .attr("id", function(d){
            return (d.name.replace(/\s+/g,'').toLowerCase());
        })
        .attr("r", function(d) {
            return 10;
        })
        .attr("fill", function(d) {
            if (d.weight > 5) {
              return "#2b8cbe";
            }
            else if (d.weight > 3) {
              return "#a6bddb";
            }
            else {
              return "#ece7f2";
            }
        });

    node.append("text")
        .attr("id", "title")
        .text(function(d){
            return `___ ${d.name}`;
        });

    node.on("dblclick", function(d){
        d.fx = null;
        d.fy = null;

        if (d.weight > 5) {
          d3.select(this).select("circle").attr("fill", "#2b8cbe");
        }
        else if (d.weight > 3) {
          d3.select(this).select("circle").attr("fill", "#a6bddb");
        }
        else {
          d3.select(this).select("circle").attr("fill", "#ece7f2");
        }

        const url = `http://localhost:5000/recommend_from_library/${d.pandas_index}`
        fetch(url)
            .then(response => response.json())
            .then(json => {
                json['query'] = {
                    'score': 0,
                    'title': d.name,
                    'pandas_index': d.pandas_index,
                }
                expand_force_graph(json);
            })
    });

    // add the curvy lines
    function tick() {
        path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                d.source.x + "," +
                d.source.y + "A" +
                dr + "," + dr + " 0 0,1 " +
                d.target.x + "," +
                d.target.y;
        });

        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    };

    function dragstarted(d) {
        if (!d3.event.active) force.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    };

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    };

    function dragended(d) {
        if (!d3.event.active) force.alphaTarget(0);
        d.fixed = true;
        if (d.fixed == true) {
            d.fx = d.x;
            d.fy = d.y;
            d3.select(this).select("circle").attr("fill", "#e127f2");
        }
        else {
            d.fx = null;
            d.fy = null;
        }
    };
}

function expand_force_graph(recommendations) {
    let links = [];
    let nodes = {};
    let width = window.innerWidth, height = 800;

    // compute the distinct nodes from the links.
    for (let key in recommendations) {
        links.push({
            "source": nodes['query'] || (nodes['query'] = {name: recommendations['query'].title, pandas_index: -1}),
            "target": nodes[key] || (nodes[key] = {name: recommendations[key].title, pandas_index: recommendations[key].pandas_index}),
            "distance": recommendations[key].score
        })
    }

    let force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(function(link) {
            return 2 ** link.distance;
        }))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-300).distanceMax(100))
        .alphaTarget(1)
        .on("tick", tick);

    let svg = d3.select("body").select("svg")

    // add the links
    let path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("id", function(d) { return d.value == 0 ? "similar" : "not-similar"; })
        .attr("class", function(d) { return "link " + d.type; });

    // define the nodes
    let node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", function(d) {
            if (d.index == Object.keys(recommendations).length - 1) {
                return "query node";
            }
            return `node-${d.pandas_index}`;
        })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

    // add the nodes
    node.append("circle")
        .attr("id", function(d){
            return (d.name.replace(/\s+/g,'').toLowerCase());
        })
        .attr("r", function(d) {
            return 10;
        })
        .attr("fill", function(d) {
            if (d.weight > 5) {
              return "#2b8cbe";
            }
            else if (d.weight > 3) {
              return "#a6bddb";
            }
            else {
              return "#ece7f2";
            }
        });

    node.append("text")
        .attr("id", "title")
        .text(function(d){
            return `___ ${d.name}`;
        });

    node.on("dblclick", function(d){
        d.fx = null;
        d.fy = null;

        if (d.weight > 5) {
          d3.select(this).select("circle").attr("fill", "#2b8cbe");
        }
        else if (d.weight > 3) {
          d3.select(this).select("circle").attr("fill", "#a6bddb");
        }
        else {
          d3.select(this).select("circle").attr("fill", "#ece7f2");
        }

        const url = `http://localhost:5000/recommend_from_library/${d.pandas_index}`
        fetch(url)
            .then(response => response.json())
            .then(json => {
                json['query'] = {
                    'score': 0,
                    'title': d.name,
                    'pandas_index': d.pandas_index,
                }
                expand_force_graph(json);
            })
    });

    // add the curvy lines
    function tick() {
        path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                d.source.x + "," +
                d.source.y + "A" +
                dr + "," + dr + " 0 0,1 " +
                d.target.x + "," +
                d.target.y;
        });

        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    };

    function dragstarted(d) {
        if (!d3.event.active) force.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    };

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    };

    function dragended(d) {
        if (!d3.event.active) force.alphaTarget(0);
        d.fixed = true;
        if (d.fixed == true) {
            d.fx = d.x;
            d.fy = d.y;
            d3.select(this).select("circle").attr("fill", "#e127f2");
        }
        else {
            d.fx = null;
            d.fy = null;
        }
    };
}
