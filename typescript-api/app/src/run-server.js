"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var index_1 = require("./index");
index_1.app.listen({ port: 3000 }, function (err) {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    console.log("\n  \uD83D\uDE80 Server ready at: http://localhost:3000\n  \u2B50\uFE0F See sample requests: http://pris.ly/e/ts/rest-fastify#3-using-the-rest-api");
});
//# sourceMappingURL=run-server.js.map