import { useState } from "react";
import type { RecordDTO } from "@/types/RecordDTO";
import { MermaidDiagram } from "./MermaidDiagram";

const getRiskColor = (level: string) => {
  switch (level) {
    case "HIGH":
      return "bg-red-100 text-red-600";
    case "MEDIUM":
      return "bg-yellow-100 text-yellow-600";
    case "LOW":
      return "bg-green-100 text-green-600";
    default:
      return "bg-gray-100 text-gray-600";
  }
};

export const RecordRow = ({ record }: { record: RecordDTO }) => {
  const [open, setOpen] = useState(false);
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="border-b last:border-none">
      {/* ROW */}
      <div
        onClick={() => setOpen((p) => !p)}
        className="grid grid-cols-12 px-4 py-3 items-center text-sm cursor-pointer hover:bg-gray-50 transition"
      >
        {/* Transaction */}
        <div className="col-span-4 font-medium truncate">
          {record.transactionId}
        </div>

        {/* Timestamp */}
        <div className="col-span-2 text-gray-500">
          {new Date(record.timestamp).toLocaleString()}
        </div>

        {/* Score */}
        <div className="col-span-4">
          <div className="flex items-center gap-2">
            <div className="w-full h-2 bg-gray-200 rounded">
              <div
                className="h-2 bg-gray-800 rounded"
                style={{ width: `${record.fraud_score * 100}%` }}
              />
            </div>
            <span className="text-xs text-gray-600 w-10 text-right">
              {record.fraud_score.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Risk */}
        <div className="col-span-1 ml-6">
          <span
            className={`px-2 py-1 text-xs rounded-md font-medium ${getRiskColor(
              record.risk_level
            )}`}
          >
            {record.risk_level}
          </span>
        </div>

        {/* Status */}
        <div className="col-span-1 text-right">
          {record.isFraud ? (
            <span className="text-red-500 text-xs font-semibold">Fraud</span>
          ) : (
            <span className="text-gray-400 text-xs">OK</span>
          )}
        </div>
      </div>

      {/* EXPANDED PANEL */}
      {open && (
        <div className="px-4 pb-4 pt-2 bg-gray-50 text-sm">
          <div className="grid md:grid-cols-2 gap-4">
            {/* LEFT */}
            <div>
              <p className="text-xs text-gray-500 mb-1">Reason</p>
              <p className="mb-3">{record.reason}</p>

              {record.pattern && (
                <>
                  <p className="text-xs text-gray-500 mb-1">Pattern</p>
                  <p className="mb-3">{record.pattern}</p>
                </>
              )}

              <p className="text-xs text-gray-500 mb-1">Related IDs</p>
              <pre className="text-xs bg-white border p-2 rounded overflow-auto">
                {JSON.stringify(record.related_ids, null, 2)}
              </pre>

                <div className="mt-4">
                    <button
                    onClick={(e) => {
                    e.stopPropagation();
                    setShowModal(true);
                    }}
                    className="text-sm font-medium px-3 py-2 rounded-md bg-gray-900 text-white hover:bg-gray-800 transition"
                    >
                    Review & Take Action
                    </button>
                </div>
            </div>

            {/* RIGHT */}
            {record.diagram && (
              <div className="bg-white border rounded p-2">
                <MermaidDiagram chart={record.diagram} />
              </div>
            )}
          </div>
        </div>
      )}

      {showModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm"
          onClick={() => setShowModal(false)}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-lg bg-white rounded-xl shadow-xl border border-gray-200 p-5"
          >
            {/* Header */}
            <h2 className="text-lg font-semibold mb-2">
              Human Intervention Required
            </h2>
            <p className="text-sm text-gray-500 mb-4">
              Review the transaction and confirm the outcome.
            </p>

            {/* Summary */}
            <div className="text-sm mb-4 space-y-2">
              <div>
                <span className="text-gray-500">Transaction:</span>{" "}
                {record.transactionId}
              </div>
              <div>
                <span className="text-gray-500">Score:</span>{" "}
                {record.fraud_score.toFixed(2)}
              </div>
              <div>
                <span className="text-gray-500">Risk:</span>{" "}
                {record.risk_level}
              </div>
            </div>

            {/* Note */}
            <textarea
              placeholder="Add optional note..."
              className="w-full border rounded-md p-2 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-gray-300"
            />

            {/* Actions */}
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowModal(false)}
                className="px-3 py-2 text-sm rounded-md border border-gray-300 hover:bg-gray-100"
              >
                Cancel
              </button>

              <button
                onClick={() => {
                  console.log("Marked SAFE", record.transactionId);
                  setShowModal(false);
                }}
                className="px-3 py-2 text-sm rounded-md bg-green-600 text-white hover:bg-green-500"
              >
                Mark Safe
              </button>

              <button
                onClick={() => {
                  console.log("Marked FRAUD", record.transactionId);
                  setShowModal(false);
                }}
                className="px-3 py-2 text-sm rounded-md bg-red-600 text-white hover:bg-red-500"
              >
                Confirm Fraud
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};