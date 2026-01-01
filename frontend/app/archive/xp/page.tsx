"use client";

import { useEffect, useState } from "react";
import { ColumnDef } from "@tanstack/react-table";
import DataTable from "@/components/data-table";
import ColorizedText from "@/components/colorized-text";
import api from "@/lib/api";

interface XPEntry {
  acc: string;
  name: string;
  xp: number;
}

interface XPSuccessResponse {
  timestamp: number;
  data: XPEntry[];
}

interface XPErrorResponse {
  detail: string;
}

type XPResponse = XPSuccessResponse | XPErrorResponse;

const columns: ColumnDef<XPEntry>[] = [
  {
    accessorKey: "name",
    header: "Player",
    cell: (info) => <ColorizedText text={info.getValue() as string} />,
  },
  {
    accessorKey: "xp",
    header: "XP",
    cell: (info) => (info.getValue() as number).toLocaleString(),
  },
];

export default function XPLeaderboardPage() {
  const [data, setData] = useState<XPEntry[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>("");
  const [actualTimestamp, setActualTimestamp] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async (timestamp: number) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.get<XPResponse>(
        `/v1/archive/xp_leaderboard/${timestamp}`,
      );
      if ("data" in response.data) {
        setData(response.data.data);
        setActualTimestamp(response.data.timestamp);
      } else {
        setData([]);
        setActualTimestamp(null);
        setError(response.data.detail);
      }
    } catch (err) {
      console.error("Failed to fetch XP leaderboard:", err);
      setError("Failed to load data");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const now = new Date();
    const localIso = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 16);
    setSelectedDate(localIso);

    const timestamp = Math.floor(now.getTime() / 1000);
    fetchData(timestamp);
  }, []);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const dateStr = e.target.value;
    setSelectedDate(dateStr);
    if (dateStr) {
      const date = new Date(dateStr);
      const timestamp = Math.floor(date.getTime() / 1000);
      fetchData(timestamp);
    }
  };

  return (
    <div className="container-xl p-4">
      <h1 className="page-title">XP Leaderboard Archive</h1>
      <p className="text-muted">
        Take a look in the past, how the XP Leaderboard looked like!
      </p>
      <div className="alert alert-info" role="alert">
        <div className="alert-icon">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="icon alert-icon icon-2"
          >
            <path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" />
            <path d="M12 9h.01" />
            <path d="M11 12h1v4h1" />
          </svg>
        </div>
        <div>
          <h4 className="alert-heading">Archive details</h4>
          <div className="alert-description">
            Data starts on April 9th 2025. Server doesn't save the leaderboard
            every minute, you will get the closest snapshot of data to the time
            you select below. If there is a big difference between the date you
            selected and the snapshot you get, it is probably because the server
            was experiencing downtime.
          </div>
          <div className="alert-description">
            <b>Select date and time in UTC timzone.</b>
          </div>
        </div>
      </div>
      <div className="mt-4 mb-4">
        <label className="form-label">Select Date & Time</label>
        <input
          type="datetime-local"
          className="form-control"
          value={selectedDate}
          onChange={handleDateChange}
        />
      </div>

      {isLoading ? (
        <div className="text-center py-5">
          <div className="spinner-border" role="status"></div>
        </div>
      ) : error ? (
        <div className="alert alert-warning">
          {error}. You can only select months starting with August 2025.
        </div>
      ) : actualTimestamp !== null ? (
        <>
          <p className="text-muted">
            Showing data for {new Date(actualTimestamp * 1000).toLocaleString()}{" "}
            your timezone (snapped at {actualTimestamp})
          </p>
          <DataTable
            data={data}
            columns={columns}
            defaultSort={[{ id: "xp", desc: true }]}
            title="XP Leaderboard"
          />
        </>
      ) : null}
    </div>
  );
}
