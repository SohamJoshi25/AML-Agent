import { RecordRow } from "@/components/layout/RecordRow";
import type { RecordDTO } from "@/types/RecordDTO";
import { useEffect, useState } from "react";

const fetchRecords = async (): Promise<RecordDTO[]> => {
  const res = await fetch("http://localhost:9000/api/records");
  return res.json();
};

const useEventStream = <T,>(onMessage: (data: T) => void) => {
  useEffect(() => {
    const eventSource = new EventSource("http://localhost:9000/api/records/events");

    eventSource.onmessage = (event) => {
      const parsed: T = JSON.parse(event.data);
      onMessage(parsed);
    };

    eventSource.onerror = (err) => {
      console.error("SSE error", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);
};

const Dashboard = () => {
  const [records, setRecords] = useState<RecordDTO[]>([]);

  useEffect(() => {
    fetchRecords().then(setRecords);
  }, []);

  // Live updates
  useEventStream<RecordDTO>((newRecord) => {
    setRecords((prev) => [newRecord, ...prev.slice(0, 29)]);
  });

  return (
  <div className="p-6 bg-gray-50 min-h-screen text-gray-900">
    <h1 className="text-2xl font-semibold mb-6">Fraud Dashboard</h1>

    <div className="rounded-xl border border-gray-200 bg-white overflow-hidden">
      <div className="grid grid-cols-12 px-4 py-3 text-xs font-medium text-gray-500 border-b bg-gray-50">
        <div className="col-span-4">Transaction</div>
        <div className="col-span-2">Timestamp</div>
        <div className="col-span-4">Score</div>
        <div className="col-span-1 ml-8">Risk</div>
        <div className="col-span-1 text-right">Status</div>
      </div>

      {records.map((record) => (
        <RecordRow key={record.transactionId} record={record} />
      ))}
    </div>
  </div>
  );
};

export default Dashboard;