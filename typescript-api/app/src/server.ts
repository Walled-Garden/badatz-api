import { PrismaClient } from "@prisma/client";
import fastify from "fastify";
import formbody from "@fastify/formbody";
import { Response__test_items } from "./types.js";
import cors from "@fastify/cors";

const prisma = new PrismaClient();
// export const app = Fastify().withTypeProvider<TypeBoxTypeProvider>({ logger: true });
export const app = fastify({ logger: true });
await app.register(cors, {
  origin: "*",
  // put your options here
});

app.register(formbody);

const stringify = (obj: any) =>
  JSON.stringify(obj, (_, v) => (typeof v === "bigint" ? v.toString() : v));

app.post<{ Body: { launch_id: number; Reply: Response__test_items } }>(
  "/test_items",
  async (req, res) => {
    const body = req.body;
    if (!body?.launch_id) {
      return res.send("no launch_id");
    }
    const test_items = await prisma.test_item.findMany({
      where: { AND: [{ launch_id: body.launch_id, parent_id: null }] },
      orderBy: { item_id: "asc" },
      select: {
        launch: {
          select: {
            id: true,
            name: true,
            number: true,
          },
        },
        item_id: true,
        test_item_results: {
          select: {
            status: true,
          },
        },
        item_attribute: {
          select: {
            value: true,
            key: true,
          },
        },
        // // todo: add parameter info as well
        // parameter: {
        //   select: {
        //     value: true,
        //     key: true,
        //   },
        // },
      },
    });

    const parsed_test_items = test_items.map((item) => {
      const parsed_item = {
        // ...item,
        item_id: item.item_id,
        ...item.test_item_results,
        attributes: item.item_attribute.reduce(
          (acc: { [key: string]: any }, curr) => {
            if (curr.key === null) {
              return acc;
            }
            acc[curr.key] = curr.value;

            return acc;
          },
          {},
        ),
        launch: item.launch,

        // parameter: item.parameter,
      };
      return parsed_item;
    });

    // Sending the JSON object as a response
    return res
      .header("Content-Type", "application/json")
      .send(stringify(parsed_test_items));
  },
);

app.get("/hey", async (req, res) => {
  return res.send("hey");
});

//app.post<{
//   Body: ISignupBody;
// }>(`/signup`, async (req, res) => {
//   const { name, email, posts } = req.body;
//
//   const postData = posts?.map((post: Prisma.PostCreateInput) => {
//     return { title: post?.title, content: post?.content };
//   });
//
//   const result = await prisma.user.create({
//     data: {
//       name,
//       email,
//       posts: {
//         create: postData
//       }
//     }
//   });
//   return result;
// });
//
// app.post<{
//   Body: ICreatePostBody;
// }>(`/post`, async (req, res) => {
//   const { title, content, authorEmail } = req.body;
//   const result = await prisma.post.create({
//     data: {
//       title,
//       content,
//       author: { connect: { email: authorEmail } }
//     }
//   });
//   return result;
// });
//
// app.put<{
//   Params: IPostByIdParam;
// }>("/post/:id/views", async (req, res) => {
//   const { id } = req.params;
//
//   try {
//     const post = await prisma.post.update({
//       where: { id: Number(id) },
//       data: {
//         viewCount: {
//           increment: 1
//         }
//       }
//     });
//
//     return post;
//   } catch (error) {
//     return { error: `Post with ID ${id} does not exist in the database` };
//   }
// });
//
// app.put<{
//   Params: IPostByIdParam;
// }>("/publish/:id", async (req, res) => {
//   const { id } = req.params;
//
//   try {
//     const postData = await prisma.post.findUnique({
//       where: { id: Number(id) },
//       select: {
//         published: true
//       }
//     });
//
//     const updatedPost = await prisma.post.update({
//       where: { id: Number(id) || undefined },
//       data: { published: !postData?.published }
//     });
//     return updatedPost;
//   } catch (error) {
//     return { error: `Post with ID ${id} does not exist in the database` };
//   }
// });
//
// app.delete<{
//   Params: IPostByIdParam;
// }>(`/post/:id`, async (req, res) => {
//   const { id } = req.params;
//   const post = await prisma.post.delete({
//     where: {
//       id: Number(id)
//     }
//   });
//   return post;
// });
//
// app.get("/users", async (req, res) => {
//   const users = await prisma.user.findMany();
//   return users;
// });
//
// app.get<{
//   Params: IPostByIdParam;
// }>("/user/:id/drafts", async (req, res) => {
//   const { id } = req.params;
//
//   const drafts = await prisma.user
//     .findUnique({
//       where: { id: Number(id) }
//     })
//     .posts({
//       where: { published: false }
//     });
//
//   return drafts;
// });
//
// app.get<{
//   Params: IPostByIdParam;
// }>(`/post/:id`, async (req, res) => {
//   const { id } = req.params;
//
//   const post = await prisma.post.findUnique({
//     where: { id: Number(id) }
//   });
//   return post;
// });
//
// app.get<{
//   Querystring: IFeedQueryString;
// }>("/feed", async (req, res) => {
//   const { searchString, skip, take, orderBy } = req?.query;
//
//   const or: Prisma.PostWhereInput = searchString
//     ? {
//         OR: [
//           { title: { contains: searchString as string } },
//           { content: { contains: searchString as string } }
//         ]
//       }
//     : {};
//
//   const posts = await prisma.post.findMany({
//     where: {
//       published: true,
//       ...or
//     },
//     include: { author: true },
//     take: Number(take) || undefined,
//     skip: Number(skip) || undefined,
//     orderBy: {
//       updatedAt: orderBy as Prisma.SortOrder
//     }
//   });
//
//   return posts;
// });
//
// interface IFeedQueryString {
//   searchString: string | null;
//   skip: number | null;
//   take: number | null;
//   orderBy: Prisma.SortOrder | null;
// }
//
// interface IPostByIdParam {
//   id: number;
// }
//
// interface ICreatePostBody {
//   title: string;
//   content: string | null;
//   authorEmail: string;
// }
//
// interface ISignupBody {
//   name: string | null;
//   email: string;
//   posts: Prisma.PostCreateInput[];
// }
