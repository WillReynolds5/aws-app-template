import { UserAuthForm } from "@/components/AuthForm";

export default function AuthenticationPage() {
  return (
    <div className="container flex min-h-screen items-center justify-center">
      <div className="mx-auto w-full max-w-[350px] space-y-6">
        <div className="flex flex-col space-y-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">Welcome</h1>
          <p className="text-sm text-muted-foreground">
            Sign in or create an account
          </p>
        </div>
        <UserAuthForm />
      </div>
    </div>
  );
}
