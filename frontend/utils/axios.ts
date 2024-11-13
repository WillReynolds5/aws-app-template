import axios from "axios";

import { cognitoUserPoolsTokenProvider } from "aws-amplify/auth/cognito";

const baseURL = process.env.NEXT_PUBLIC_API_ENDPOINT;

// Create an instance for non-authenticated requests
export const apiPublic = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Create an instance for authenticated requests
export const apiAuth = axios.create({
  baseURL,
});

// Interceptor for authenticated requests
apiAuth.interceptors.request.use(
  async (config) => {
    const tokens = await cognitoUserPoolsTokenProvider.getTokens();
    if (tokens?.accessToken) {
      config.headers[
        "Authorization"
      ] = `Bearer ${tokens.accessToken.toString()}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

[apiPublic, apiAuth].forEach((instance) => {
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      // Handle errors (e.g., refresh token, logout on 401, etc.)
      if (error.response && error.response.status === 401) {
        // Handle unauthorized access
        // For example: redirect to login page
      }
      return Promise.reject(error);
    }
  );
});
