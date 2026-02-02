"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";

const taskSchema = z.object({
  title: z.string().min(1, "Title is required"),
  estimated_completion_time: z
    .string()
    .optional()
    .transform((value) => (value ? new Date(value).toISOString() : undefined)),
});

type TaskFormValues = z.infer<typeof taskSchema>;

type Task = {
  id: number;
  title: string;
  completed: boolean;
  estimated_completion_time?: string | null;
};

type CurrentUser = {
  id: number;
  email: string;
  nickname: string;
};

export default function HomePage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [token, setToken] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [otpCode, setOtpCode] = useState<string>("");
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [otpInfo, setOtpInfo] = useState<string | null>(null);

  const form = useForm<TaskFormValues>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: "",
      estimated_completion_time: "",
    },
  });

  const fetchTasks = async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.get<Task[]>("/tasks/");
      setTasks(data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const fetchCurrentUser = async () => {
    if (!token) {
      setCurrentUser(null);
      return;
    }
    try {
      const { data } = await api.get<CurrentUser>("/auth/me");
      setCurrentUser(data);
    } catch {
      // Invalid token – clear it
      setCurrentUser(null);
      setToken("");
    }
  };

  useEffect(() => {
    // Persist token for axios interceptor
    if (typeof window !== "undefined") {
      if (token) {
        localStorage.setItem("access_token", token);
      } else {
        localStorage.removeItem("access_token");
      }
    }
    void fetchTasks();
    void fetchCurrentUser();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  const handleRequestOtp = async () => {
    if (!email) {
      setError("Please enter your email first.");
      return;
    }
    setLoading(true);
    setError(null);
    setOtpInfo(null);
    try {
      const { data } = await api.post("/auth/request-otp", { email });
      // Backend returns OTP in response for demo purposes
      if (data.otp) {
        setOtpInfo(`OTP (dev only): ${data.otp}`);
      } else {
        setOtpInfo("OTP requested. Check backend logs/email.");
      }
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleLoginWithOtp = async () => {
    if (!email || !otpCode) {
      setError("Please enter both email and OTP code.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.post<{ access_token: string }>(
        "/auth/login-otp",
        { email, code: otpCode },
      );
      setToken(data.access_token);
      setOtpCode("");
      setAuthModalOpen(false);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = async (values: TaskFormValues) => {
    if (!token) {
      setError("Please paste your access token first.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await api.post("/tasks/", values);
      form.reset();
      await fetchTasks();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-background">
      {/* Auth modal */}
      {authModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-md rounded-lg border bg-card p-6 shadow-lg">
            <h2 className="mb-4 text-lg font-semibold">Login / Signup</h2>

            <div className="space-y-3">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <Button
                  type="button"
                  disabled={loading}
                  onClick={handleRequestOtp}
                >
                  {loading ? "Requesting OTP..." : "Request OTP (signup / login)"}
                </Button>
                {otpInfo && (
                  <p className="text-xs text-muted-foreground">
                    {otpInfo}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="otp">OTP code</Label>
                <Input
                  id="otp"
                  placeholder="6-digit code"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                />
                <Button
                  type="button"
                  disabled={loading}
                  onClick={handleLoginWithOtp}
                >
                  {loading ? "Logging in..." : "Login with OTP"}
                </Button>
              </div>

              <div className="space-y-2">
                <Label htmlFor="token">Access token (JWT)</Label>
                <Input
                  id="token"
                  placeholder="Will be filled after login, or paste manually"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setAuthModalOpen(false)}
                >
                  Close
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="mx-auto flex max-w-2xl flex-col gap-6 px-4 py-10">
        <header className="flex items-center justify-between">
          <div className="space-y-1">
            <h1 className="text-2xl font-bold">Todo App</h1>
            <p className="text-sm text-muted-foreground">
              FastAPI backend at <code>http://127.0.0.1:8000</code>, Next.js frontend at{" "}
              <code>http://localhost:3000</code>.
            </p>
          </div>
          <div className="flex items-center gap-3">
            {currentUser ? (
              <div className="text-right text-xs">
                <p className="font-medium">{currentUser.nickname}</p>
                <p className="text-muted-foreground">{currentUser.email}</p>
              </div>
            ) : null}
            <Button
              type="button"
              variant="outline"
              onClick={() => setAuthModalOpen(true)}
            >
              {currentUser ? "Change account" : "Login"}
            </Button>
          </div>
        </header>

        <section className="space-y-4 rounded-lg border bg-card p-4">
          <h2 className="text-sm font-semibold">Create task</h2>
          <form
            className="space-y-3"
            onSubmit={form.handleSubmit(onSubmit)}
            noValidate
          >
            <div className="space-y-1">
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                {...form.register("title")}
                placeholder="Buy milk"
              />
              {form.formState.errors.title && (
                <p className="text-xs text-red-500">
                  {form.formState.errors.title.message}
                </p>
              )}
            </div>

            <div className="space-y-1">
              <Label htmlFor="estimated_completion_time">
                Estimated completion time (optional)
              </Label>
              <Input
                id="estimated_completion_time"
                type="datetime-local"
                {...form.register("estimated_completion_time")}
              />
            </div>

            <Button type="submit" disabled={loading}>
              {loading ? "Saving..." : "Add task"}
            </Button>
          </form>
        </section>

        <section className="space-y-3 rounded-lg border bg-card p-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold">Your tasks</h2>
            <Button variant="outline" type="button" onClick={() => fetchTasks()}>
              Refresh
            </Button>
          </div>

          {error && <p className="text-sm text-red-500">{error}</p>}

          {loading && <p className="text-sm text-muted-foreground">Loading...</p>}

          <ul className="space-y-2">
            {tasks.map((task) => (
              <li
                key={task.id}
                className="flex items-start justify-between rounded-md border bg-background px-3 py-2 text-sm"
              >
                <div>
                  <p className={task.completed ? "line-through opacity-60" : ""}>
                    {task.title}
                  </p>
                  {task.estimated_completion_time && (
                    <p className="text-xs text-muted-foreground">
                      Estimated completion:{" "}
                      {new Date(
                        task.estimated_completion_time,
                      ).toLocaleString()}
                    </p>
                  )}
                </div>
                <span
                  className={`ml-2 rounded-full px-2 py-0.5 text-xs ${
                    task.completed
                      ? "bg-green-100 text-green-700"
                      : "bg-yellow-100 text-yellow-700"
                  }`}
                >
                  {task.completed ? "Completed" : "Pending"}
                </span>
              </li>
            ))}
            {!tasks.length && !loading && (
              <p className="text-sm text-muted-foreground">
                No tasks yet. Create your first task above.
              </p>
            )}
          </ul>
        </section>
      </div>
    </main>
  );
}

