import type { RecordDTO } from "@/types/RecordDTO";
import { MermaidDiagram } from "./MermaidDiagram";


const getRiskColor = (level: string) => {
  switch (level) {
    case "HIGH":
      return "bg-red-500/20 text-red-400";
    case "MEDIUM":
      return "bg-yellow-500/20 text-yellow-400";
    case "LOW":
      return "bg-green-500/20 text-green-400";
    default:
      return "bg-gray-500/20 text-gray-300";
  }
};

export const RecordCard = ({ record }: { record: RecordDTO }) => {
  return (
    <div className="rounded-2xl bg-gray-900 p-4 shadow-lg border border-gray-800 hover:border-gray-600 transition">
      
      {/* Header */}
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm opacity-70">
          {new Date(record.timestamp).toLocaleString()}
        </span>

        <span
          className={`px-2 py-1 text-xs rounded ${getRiskColor(
            record.risk_level
          )}`}
        >
          {record.risk_level}
        </span>
      </div>

      {record.diagram && (
        <div className="mt-3 bg-black p-2 rounded">
          <MermaidDiagram chart={record.diagram} />
        </div>
      )}

      {/* Fraud Score */}
      <div className="mb-2">
        <span className="text-lg font-semibold">
          Score: {record.fraud_score.toFixed(2)}
        </span>
      </div>

      {/* Reason */}
      <p className="text-sm opacity-80 mb-2">{record.reason}</p>

      {/* Fraud flag */}
      {record.isFraud && (
        <div className="text-red-400 text-sm font-semibold">
          🚨 Fraud Detected
        </div>
      )}
    </div>
  );
};