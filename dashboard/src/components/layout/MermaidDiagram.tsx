import mermaid from "mermaid";
import { useEffect, useRef } from "react";

export const MermaidDiagram = ({ chart }: { chart: string }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    mermaid.initialize({ startOnLoad: false });

    const renderDiagram = async () => {
      if (!ref.current) return;

      try {
        const id = `mermaid-${Math.random().toString(36).slice(2)}`;
        const { svg } = await mermaid.render(id, chart);

        ref.current.innerHTML = svg;
      } catch (err) {
        console.error("Mermaid render error:", err);
      }
    };

    renderDiagram();
  }, [chart]);

  return <div ref={ref} />;
};