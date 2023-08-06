<!-- Copyright 2021 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div class="card" ref="container">
    <div class="toolbar mt-1 mr-1">
      <i class="fas fa-circle-notch fa-spin text-muted mr-2" v-if="loading"></i>
      <button title="Decrease link depth"
              type="button"
              class="btn btn-link text-muted"
              :disabled="depth <= 1"
              @click="depth--">
        <i class="fas fa-chevron-left"></i>
      </button>
      <strong class="text-muted">Link depth: {{ depth }}</strong>
      <button title="Increase link depth"
              type="button"
              class="btn btn-link text-muted"
              :disabled="depth >= 3"
              @click="depth++">
        <i class="fas fa-chevron-right"></i>
      </button>
      <button title="Reset view" type="button" class="btn btn-link text-muted" @click="resetView">
        <i class="fas fa-eye"></i>
      </button>
      <button title="Toggle fullscreen" type="button" class="btn btn-link text-muted" @click="toggleFullscreen">
        <i class="fas fa-expand"></i>
      </button>
    </div>
    <div ref="svgContainer"></div>
  </div>
</template>

<style scoped>
.toolbar {
  position: absolute;
  right: 0;
  z-index: 1;
}
</style>

<script>
import * as d3 from 'd3';

export default {
  data() {
    return {
      svg: null,
      legendContainer: null,
      graphContainer: null,
      zoom: null,
      simulation: null,
      nodes: [],
      links: [],
      excludedTypes: [],
      width: 0,
      height: 0,
      depth: 1,
      loading: true,
      timeoutHandle: null,
      suffix: kadi.utils.randomAlnum(),
    };
  },
  props: {
    endpoint: String,
    startRecord: Number,
    filter: {
      type: String,
      default: '',
    },
    isRendered: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    depth() {
      this.loading = true;

      if (this.timeoutHandle !== null) {
        clearTimeout(this.timeoutHandle);
      }
      this.timeoutHandle = setTimeout(() => this.updateData(), 500);
    },
    filter() {
      this.filterNodes();
    },
    isRendered() {
      this.resizeView(false);
    },
  },
  methods: {
    isFullscreen() {
      return document.fullScreen || document.mozFullScreen || document.webkitIsFullScreen;
    },
    isNodeVisible(id) {
      return this.graphContainer.select(`#node-${id}-${this.suffix}`).style('visibility') === 'visible';
    },
    getTypeColor(scale, type, darker = false) {
      const color = type === null ? 'grey' : scale(type);
      return darker ? d3.color(color).darker(1) : color;
    },
    centerStartNode() {
      const startNode = this.nodes.filter((item) => item.id === this.startRecord)[0];
      if (startNode) {
        startNode.fx = this.width * 0.6;
        startNode.fy = this.height * 0.5;
      }
    },
    resetView() {
      this.centerStartNode();
      this.zoom.scaleTo(this.svg, 1);
      this.zoom.translateTo(this.svg, 0, 0, [0, 0]);
      this.simulation.alpha(1).restart();
    },
    toggleFullscreen() {
      if (this.isFullscreen()) {
        document.exitFullscreen();
      } else {
        this.$refs.container.requestFullscreen();
      }
    },
    resizeView(resetView = true) {
      // In case the component is not marked as rendered from the outside we do not attempt to resize it.
      if (!this.isRendered) {
        return;
      }

      this.width = this.$refs.container.getBoundingClientRect().width - 2;
      this.height = Math.round(window.innerHeight / window.innerWidth * this.width);

      if (this.isFullscreen()) {
        this.$refs.svgContainer.style.height = '100vh';
        this.$refs.container.style.borderRadius = '0';
      } else {
        this.$refs.svgContainer.style.height = `${this.height}px`;
        this.$refs.container.style.borderRadius = '0.25rem';
      }

      // Take the border width into account as well
      this.svg.attr('width', this.width).attr('height', this.height);

      if (resetView) {
        this.resetView();
      }
    },
    filterNodes() {
      this.graphContainer.selectAll(`.node-${this.suffix}`).each((d, i, nodes) => {
        const node = d3.select(nodes[i]);

        if (this.excludedTypes.includes(d.type)) {
          node.style('visibility', 'hidden');
        } else {
          if (d.identifier.includes(this.filter.trim())) {
            node.style('visibility', 'visible');
          } else {
            node.style('visibility', 'hidden');
          }
        }
      });

      this.graphContainer.selectAll(`.link-${this.suffix}`).each((d, i, nodes) => {
        const link = d3.select(nodes[i]);

        if (this.isNodeVisible(d.source.id) && this.isNodeVisible(d.target.id)) {
          link.style('visibility', 'visible');
        } else {
          link.style('visibility', 'hidden');
        }
      });
    },
    toggleType(type) {
      let opacity = 0;

      if (this.excludedTypes.includes(type)) {
        kadi.utils.removeFromList(this.excludedTypes, type);
        opacity = 1;
      } else {
        this.excludedTypes.push(type);
        opacity = 0.3;
      }

      this.legendContainer.selectAll('circle').filter((d) => d === type).style('opacity', opacity);
      this.filterNodes();
    },
    getBezierPoints(d) {
      const dx = d.target.x - d.source.x;
      const dy = d.target.y - d.source.y;
      return {
        x1: d.source.x,
        y1: d.source.y,
        x2: d.source.x + (dx / 2) + (dy / 5 * d.link_index),
        y2: d.source.y + (dy / 2) - (dx / 5 * d.link_index),
        x3: d.target.x,
        y3: d.target.y,
      };
    },
    quadraticBezierCurve(d) {
      const pts = this.getBezierPoints(d);
      return `M ${pts.x1},${pts.y1} Q ${pts.x2} ${pts.y2} ${pts.x3} ${pts.y3}`;
    },
    linkLabelTransformation(d) {
      const pts = this.getBezierPoints(d);

      // Calculate a good position for the text along the link path.
      const t = 0.5;
      const posX = pts.x2 + (((1 - t) ** 2) * (pts.x1 - pts.x2)) + ((t ** 2) * (pts.x3 - pts.x2));
      const posY = pts.y2 + (((1 - t) ** 2) * (pts.y1 - pts.y2)) + ((t ** 2) * (pts.y3 - pts.y2));

      // Calculate the angle of the path at this position to rotate the text properly.
      const slopeX = (2 * (1 - t) * (pts.x2 - pts.x1)) + (2 * t * (pts.x3 - pts.x2));
      const slopeY = (2 * (1 - t) * (pts.y2 - pts.y1)) + (2 * t * (pts.y3 - pts.y2));

      let rotation = Math.atan2(slopeY, slopeX) * (180 / Math.PI);
      rotation = pts.x1 > pts.x3 ? rotation - 180 : rotation;

      // Calculate an additional margin between the path and the text based on the rotation.
      const margin = pts.x1 > pts.x3 ? -15 : 5;
      const marginX = Math.sin((rotation / 180) * Math.PI) * margin;
      const marginY = Math.cos((rotation / 180) * Math.PI) * margin;

      return `translate(${posX + marginX} ${posY - marginY}) rotate(${rotation})`;
    },
    drag() {
      return d3.drag()
        .on('start', (e) => {
          if (e.subject.id !== this.startRecord) {
            if (!e.active) {
              this.simulation.alphaTarget(0.5).restart();
            }
            e.subject.fx = e.subject.x;
            e.subject.fy = e.subject.y;
          }
        })
        .on('drag', (e) => {
          if (e.subject.id !== this.startRecord) {
            e.subject.fx = e.x;
            e.subject.fy = e.y;
          }
        })
        .on('end', (e) => {
          if (e.subject.id !== this.startRecord) {
            if (!e.active) {
              this.simulation.alphaTarget(0);
            }
            e.subject.fx = null;
            e.subject.fy = null;
          }
        });
    },
    drawGraph() {
      const typesMap = new Map();
      this.nodes.forEach((node) => {
        const typeMeta = {
          count: typesMap.has(node.type) ? typesMap.get(node.type).count + 1 : 1,
          type_full: node.type_full,
        };
        typesMap.set(node.type, typeMeta);
      });

      const typesArray = Array.from(typesMap.keys());
      typesArray.sort((a, b) => (a === null) - (b === null) || Number(a > b) || -(a < b));

      const colorScale = d3.scaleOrdinal(d3.schemePaired).domain(typesArray);

      // Draw the legend.
      const legendGroup = this.legendContainer
        .selectAll()
        .data(typesArray)
        .enter()
        .append('g');

      const radius = 10;
      const padding = 8;

      legendGroup
        .append('circle')
        .attr('r', radius)
        .attr('cx', radius + padding)
        .attr('cy', (d, i) => ((i + 1) * radius) + (i * (radius + padding)) + padding)
        .style('fill', (d) => this.getTypeColor(colorScale, d))
        .style('stroke', (d) => this.getTypeColor(colorScale, d, true))
        .style('cursor', 'pointer')
        .on('click', (e) => this.toggleType(e.target.__data__));

      legendGroup
        .append('text')
        .text((d) => `${d || 'No type'} (${typesMap.get(d).count})`)
        .attr('x', (radius * 3) + padding)
        .attr('y', (d, i) => ((i + 1) * radius) + (i * (radius + padding)) + padding)
        .attr('dy', 5)
        .style('fill', (d) => this.getTypeColor(colorScale, d, true))
        .style('font-style', (d) => (d === null ? 'italic' : 'normal'))
        .style('cursor', 'default')
        .filter((d) => d !== null)
        .append('title')
        .text((d) => typesMap.get(d).type_full);

      // Draw the links.
      const linkGroup = this.graphContainer
        .selectAll()
        .data(this.links)
        .enter()
        .append('g')
        .attr('class', `link-${this.suffix}`);

      linkGroup
        .append('path')
        .attr('class', `link-path-${this.suffix}`)
        .attr('fill', 'none')
        .attr('stroke', '#c9c9c9')
        .attr('stroke-width', 3)
        .attr('marker-end', `url(#arrowhead-${this.suffix})`);

      linkGroup
        .append('text')
        .text((d) => d.name)
        .attr('class', `link-label-${this.suffix}`)
        .style('font-size', '85%')
        .style('text-anchor', 'middle')
        .style('cursor', 'default')
        .append('title')
        .text((d) => d.name_full);

      // Draw the nodes.
      const nodeGroup = this.graphContainer
        .selectAll()
        .data(this.nodes)
        .enter()
        .append('g')
        .attr('id', (d) => `node-${d.id}-${this.suffix}`)
        .attr('class', `node-${this.suffix}`)
        .call(this.drag());

      nodeGroup
        .append('circle')
        .attr('r', 15)
        .style('fill', (d) => this.getTypeColor(colorScale, d.type))
        .style('stroke', (d) => this.getTypeColor(colorScale, d.type, true))
        .style('stroke-width', 5)
        .filter((d) => d.id !== this.startRecord)
        .style('stroke-width', 2)
        .style('cursor', 'pointer');

      nodeGroup
        .append('a')
        .attr('href', (d) => d.url)
        .append('text')
        .text((d) => `@${d.identifier}`)
        .attr('dy', 30)
        .style('font-weight', 'bold')
        .style('text-anchor', 'middle')
        .on('mouseover', (e) => d3.select(e.target).style('fill', '#2c3e50'))
        .on('mouseout', (e) => d3.select(e.target).style('fill', 'black'))
        .append('title')
        .text((d) => d.identifier_full);

      nodeGroup
        .filter((d) => d.type !== null)
        .append('text')
        .text((d) => d.type)
        .attr('dy', 45)
        .style('font-size', '70%')
        .style('text-anchor', 'middle')
        .style('cursor', 'default')
        .append('title')
        .text((d) => d.type_full);

      this.centerStartNode();

      // Initialize and restart the simulation.
      this.simulation.nodes(this.nodes);
      this.simulation.force('link').links(this.links);
      this.simulation.alpha(1).restart();
    },
    updateData() {
      axios.get(this.endpoint, {params: {depth: this.depth}})
        .then((response) => {
          this.nodes = response.data.nodes;
          this.links = response.data.links;

          this.graphContainer.selectAll('*').remove();
          this.legendContainer.selectAll('*').remove();

          this.drawGraph();
          this.filterNodes();
        })
        .catch((error) => kadi.alert('Error loading record links.', {xhr: error.request}))
        .finally(() => this.loading = false);
    },
  },
  mounted() {
    this.svg = d3.select(this.$refs.svgContainer).append('svg');
    this.graphContainer = this.svg.append('g');
    this.legendContainer = this.svg.append('g');

    // Definition for the arrow heads of the links.
    this.svg.append('defs')
      .append('marker')
      .attr('id', `arrowhead-${this.suffix}`)
      .attr('viewBox', '0 0 10 10')
      .attr('refX', 19)
      .attr('refY', 4.5)
      .attr('orient', 'auto')
      .attr('markerWidth', 5)
      .attr('markerHeight', 5)
      .append('path')
      .attr('d', 'M 0 0 L 10 5 L 0 10 z')
      .style('fill', '#c9c9c9');

    this.zoom = d3.zoom().on('zoom', (e) => this.graphContainer.attr('transform', e.transform));
    this.svg.call(this.zoom).on('dblclick.zoom', null);

    this.simulation = d3.forceSimulation()
      .force('charge', d3.forceManyBody().strength(-2000))
      .force('link', d3.forceLink().id((d) => d.id).distance((d) => (d.link_length * 7) + 250))
      .on('tick', () => {
        this.graphContainer
          .selectAll(`.node-${this.suffix}`)
          .attr('transform', (d) => `translate(${d.x} ${d.y})`);
        this.graphContainer
          .selectAll(`.link-path-${this.suffix}`)
          .attr('d', (d) => this.quadraticBezierCurve(d));
        this.graphContainer
          .selectAll(`.link-label-${this.suffix}`)
          .attr('transform', (d) => this.linkLabelTransformation(d));
      });

    this.resizeView();
    this.updateData();

    window.addEventListener('resize', this.resizeView);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeView);
  },
};
</script>
