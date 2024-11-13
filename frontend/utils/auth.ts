import { getCurrentUser } from "aws-amplify/auth";

export async function getUserId(): Promise<string | null> {
  try {
    const user = await getCurrentUser();
    return user.userId;
  } catch (error) {
    return null;
  }
}
