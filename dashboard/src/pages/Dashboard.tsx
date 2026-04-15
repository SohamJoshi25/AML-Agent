import { RecordCard } from "@/components/layout/RecordCard";
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
    <div className="p-6 bg-gray-950 min-h-screen text-white">
      <h1 className="text-2xl font-semibold mb-6">Fraud Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {records.map((record) => (
          <RecordCard key={record.transactionId} record={record} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;