export type RecordDTO = {
  transactionId: string;
  timestamp: string;

  diagram?: string;
  reason: string;
  pattern?: string;

  related_ids: Record<string, unknown>;

  fraud_score: number;
  risk_level: string;
  is_fraud: boolean;
};
