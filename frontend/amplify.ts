import { Amplify } from "aws-amplify";

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID!,
      userPoolClientId: process.env.NEXT_PUBLIC_COGNITO_USER_POOL_CLIENT_ID!,
      signUpVerificationMethod: process.env
        .NEXT_PUBLIC_COGNITO_SIGN_UP_VERIFICATION_METHOD as "code" | "link",
    },
  },
});

// Optional: Add some error checking
if (
  !process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID ||
  !process.env.NEXT_PUBLIC_COGNITO_USER_POOL_CLIENT_ID
) {
  console.error(
    "Cognito User Pool configuration is missing. Please check your .env.local file."
  );
}
