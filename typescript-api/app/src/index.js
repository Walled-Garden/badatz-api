"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.app = void 0;
var client_1 = require("@prisma/client");
var fastify_1 = __importDefault(require("fastify"));
var prisma = new client_1.PrismaClient();
exports.app = (0, fastify_1.default)({ logger: true });
var stringify = function (obj) {
    return JSON.stringify(obj, function (_, v) { return (typeof v === "bigint" ? v.toString() : v); });
};
exports.app.get("/", function (req, res) { return __awaiter(void 0, void 0, void 0, function () {
    var test_items;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, prisma.test_item.findMany({
                    where: { AND: [{ launch_id: 1135, parent_id: null }] },
                    include: {
                        item_attribute: true,
                    },
                })];
            case 1:
                test_items = _a.sent();
                // const test_items = await prisma.$queryRaw`
                //       SELECT * FROM public.test_item
                //       where (nlevel("test_item"."path") = 1 and "test_item"."launch_id" = 1135)
                //       `;
                // Sending the JSON object as a response
                return [2 /*return*/, res.send(test_items.length)];
        }
    });
}); });
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
//# sourceMappingURL=index.js.map