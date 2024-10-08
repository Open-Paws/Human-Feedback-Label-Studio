import { types } from "mobx-state-tree";
import { camelizeKeys } from "../utils/utilities";

export const UserExtended = types
  .model("UserExtended", {
    id: types.identifierNumber,
    firstName: types.maybeNull(types.string),
    lastName: types.maybeNull(types.string),
    username: types.maybeNull(types.string),
    email: types.maybeNull(types.string),
    lastActivity: types.maybeNull(types.string),
    avatar: types.maybeNull(types.string),
    initials: types.maybeNull(types.string),
    phone: types.maybeNull(types.string),
    advocate: types.maybeNull(types.string),
    current_lifestyle: types.maybeNull(types.string),
    roles: types.maybeNull(types.string),
    advocacy_approach: types.maybeNull(types.integer),
    advocacy_focus: types.maybeNull(types.integer),
    advocacy_intersectionality: types.maybeNull(types.integer),
    advocacy_rights: types.maybeNull(types.integer),
    advocacy_diplomacy: types.maybeNull(types.integer),
    advocacy_empiricism: types.maybeNull(types.integer),
    // demographics
    age: types.maybeNull(types.string),
    gender: types.maybeNull(types.string),
    ethnicity: types.maybeNull(types.string),
    country: types.maybeNull(types.string),
    education_level: types.maybeNull(types.string),
    income_level: types.maybeNull(types.string),
    political_affiliation: types.maybeNull(types.string),
    religious_affiliation: types.maybeNull(types.string),
    // psychographics
    openness: types.maybeNull(types.integer),
    conscientiousness: types.maybeNull(types.integer),
    extraversion: types.maybeNull(types.integer),
    agreeableness: types.maybeNull(types.integer),
    neuroticism: types.maybeNull(types.integer),

  })
  .preProcessSnapshot((sn) => {
    return camelizeKeys(sn ?? {});
  });

/**
 * User store of Label Studio
 */
const UserStore = types
  .model("UserStore", {
    /**
     * Personal key of user
     */
    id: types.maybeNull(types.integer),
    /**
     * Personal key of user
     */
    pk: types.maybeNull(types.integer),
    /**
     * Name of user
     */
    firstName: types.maybeNull(types.string),
    /**
     * Last name of user
     */
    lastName: types.maybeNull(types.string),
  })
  .views((self) => ({
    get displayName() {
      if (self.firstName || self.lastName) return `${self.firstName} ${self.lastName}`;

      return "";
    },
  }));

export default UserStore;
