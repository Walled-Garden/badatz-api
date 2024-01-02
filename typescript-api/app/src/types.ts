// export type Response__test_items = Array<{
//   item_id: string;
//   test_item_results: {
//     status: string;
//   };
//   item_attribute: Array<{
//     value: string;
//     key: string;
//   }>;
// }>;
export type Response__test_items = TestItem[];

export interface TestItem {
  launch: Launch;
  item_id: string;
  status: string;
  attributes: Attributes;
}

export interface Launch {
  id: string;
  name: string;
  number: number;
}

export type KnownAttributeKey = "who" | "where" | "policies" | "action";
export type AttributeKey = KnownAttributeKey | string;

export type Attributes<
  Key extends AttributeKey = AttributeKey,
  Val extends string = string,
> = {
  [key in Key]: Val;
};

type t = { [key in KnownAttributeKey]: string };
