import { app } from "./index";

export const handler = async (event: any, context: any): Promise<any> => {
  const response = await app.inject({
    method: event.httpMethod,
    url: event.path,
    payload: event.body,
  });
  return {
    statusCode: response.statusCode,
    headers: response.headers,
    body: response.body,
  };
};
