"""Animation drivers for browser-captured Mermaid GIFs (injected into a local HTML page)."""

from __future__ import annotations

STYLES = ("progressive", "highlight-walk", "pulse-flow", "wave")

ELEMENT_COLLECTION = """
    var clusters = [], nodes = [], edges = [], edgeLabels = [];
    var direction = '{direction}';
    var sortFn = direction === 'horizontal'
        ? function(a, b) { return (a.x - b.x) || (a.y - b.y); }
        : function(a, b) { return (a.y - b.y) || (a.x - b.x); };
    svg.querySelectorAll('.cluster').forEach(function(el) {
        clusters.push({ el: el, x: el.getBoundingClientRect().x, y: el.getBoundingClientRect().y });
    });
    svg.querySelectorAll('.node, .actor, [class*="note"]').forEach(function(el) {
        nodes.push({ el: el, x: el.getBoundingClientRect().x, y: el.getBoundingClientRect().y });
    });
    svg.querySelectorAll('.edgePath, [class*="messageLine"], .relation').forEach(function(el) {
        edges.push({ el: el, x: el.getBoundingClientRect().x, y: el.getBoundingClientRect().y });
    });
    svg.querySelectorAll('.edgeLabel, .messageText').forEach(function(el) {
        edgeLabels.push({ el: el, x: el.getBoundingClientRect().x, y: el.getBoundingClientRect().y });
    });
    clusters.sort(sortFn); nodes.sort(sortFn); edges.sort(sortFn); edgeLabels.sort(sortFn);
    var elements = clusters.concat(nodes, edges, edgeLabels);
    if (!elements.length) {
        svg.style.opacity = '0';
        window.setProgress = function(t) { svg.style.opacity = String(Math.min(1, t * 2)); };
        window.animationReady = true;
        return;
    }
"""

STYLE_PROGRESSIVE = """
    var timeline = [];
    clusters.forEach(function(c) { timeline.push({ el: c.el, type: 'cluster' }); });
    var eIdx = 0, lIdx = 0;
    nodes.forEach(function(n) {
        timeline.push({ el: n.el, type: 'node' });
        if (eIdx < edges.length) { timeline.push({ el: edges[eIdx].el, type: 'edge' }); eIdx++; }
        if (lIdx < edgeLabels.length) { timeline.push({ el: edgeLabels[lIdx].el, type: 'label' }); lIdx++; }
    });
    while (eIdx < edges.length) { timeline.push({ el: edges[eIdx].el, type: 'edge' }); eIdx++; }
    while (lIdx < edgeLabels.length) { timeline.push({ el: edgeLabels[lIdx].el, type: 'label' }); lIdx++; }
    timeline.forEach(function(item, i) { item.appearAt = (i / timeline.length) * 0.85; });
    var dim = 0.25, activate = 0.08;
    timeline.forEach(function(item) {
        item.el.style.opacity = String(dim);
        if (item.type === 'edge') {
            var path = item.el.querySelector('path');
            if (path) {
                try {
                    var len = path.getTotalLength();
                    path.style.strokeDasharray = String(len);
                    path.style.strokeDashoffset = String(len);
                    item._path = path; item._len = len;
                } catch (e) {}
            }
        }
    });
    window.setProgress = function(t) {
        timeline.forEach(function(item) {
            if (t >= item.appearAt) {
                var local = Math.min(1, (t - item.appearAt) / activate);
                item.el.style.opacity = String(dim + (1 - dim) * local);
                if (item._path && item._len) item._path.style.strokeDashoffset = String(item._len * (1 - local));
            } else {
                item.el.style.opacity = String(dim);
                if (item._path && item._len) item._path.style.strokeDashoffset = String(item._len);
            }
        });
    };
"""

STYLE_HIGHLIGHT = """
    var timeline = [];
    clusters.forEach(function(c) { timeline.push(c.el); });
    var eIdx = 0, lIdx = 0;
    nodes.forEach(function(n) {
        timeline.push(n.el);
        if (eIdx < edges.length) { timeline.push(edges[eIdx].el); eIdx++; }
        if (lIdx < edgeLabels.length) { timeline.push(edgeLabels[lIdx].el); lIdx++; }
    });
    while (eIdx < edges.length) { timeline.push(edges[eIdx].el); eIdx++; }
    while (lIdx < edgeLabels.length) { timeline.push(edgeLabels[lIdx].el); lIdx++; }
    var triggers = timeline.map(function(el, i) {
        el.style.opacity = '0.15';
        return { el: el, at: i / timeline.length };
    });
    var spot = Math.max(0.1, 1.2 / timeline.length);
    window.setProgress = function(t) {
        triggers.forEach(function(item) {
            var dist = Math.abs(t - item.at);
            if (dist < spot / 2) {
                item.el.style.opacity = '1';
                item.el.style.filter = 'drop-shadow(0 0 8px rgba(79,90,143,0.85))';
            } else if (t > item.at + spot / 2) {
                item.el.style.opacity = '0.9';
                item.el.style.filter = 'none';
            } else {
                item.el.style.opacity = '0.15';
                item.el.style.filter = 'none';
            }
        });
    };
"""

STYLE_PULSE = """
    elements.forEach(function(item) { item.el.style.opacity = '1'; });
    var flowPaths = [];
    svg.querySelectorAll('[class*="edgePath"] path, [class*="messageLine"]').forEach(function(path) {
        try {
            var len = path.getTotalLength();
            path.style.strokeDasharray = '10 6';
            flowPaths.push({ el: path, length: len });
        } catch (e) {}
    });
    var speed = 200;
    window.setProgress = function(t) {
        flowPaths.forEach(function(fp) { fp.el.style.strokeDashoffset = String(-t * speed); });
    };
"""

STYLE_WAVE = """
    elements.forEach(function(item) { item.el.style.opacity = '1'; });
    var order = [];
    clusters.forEach(function(c) { order.push(c.el); });
    var eIdx = 0, lIdx = 0;
    nodes.forEach(function(n) {
        order.push(n.el);
        if (eIdx < edges.length) { order.push(edges[eIdx].el); eIdx++; }
        if (lIdx < edgeLabels.length) { order.push(edgeLabels[lIdx].el); lIdx++; }
    });
    while (eIdx < edges.length) { order.push(edges[eIdx].el); eIdx++; }
    while (lIdx < edgeLabels.length) { order.push(edgeLabels[lIdx].el); lIdx++; }
    var triggers = order.map(function(el, i) { return { el: el, at: (i / order.length) * 0.8 }; });
    var width = 0.10;
    window.setProgress = function(t) {
        triggers.forEach(function(item) {
            var dt = t - item.at;
            if (dt >= 0 && dt < width) {
                var phase = dt / width;
                var brightness = 1 + 0.35 * Math.sin(phase * Math.PI);
                item.el.style.filter = 'brightness(' + brightness + ') drop-shadow(0 0 6px rgba(79,90,143,0.55))';
            } else {
                item.el.style.filter = 'none';
            }
        });
    };
"""

STYLE_BODY = {
    "progressive": STYLE_PROGRESSIVE,
    "highlight-walk": STYLE_HIGHLIGHT,
    "pulse-flow": STYLE_PULSE,
    "wave": STYLE_WAVE,
}
