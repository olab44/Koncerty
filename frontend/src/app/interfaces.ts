export interface SignUpResponse {
    message: string;
    app_token: string;
    new: boolean;
  }

export interface GroupInfo {
    group_id: number;
    group_name: string;
    role: string;
    extra_info?: string;
    inv_code?: string;
    subgroups?: SubgroupInfo[];
}

export interface SubgroupInfo {
    subgroup_id: number;
    subgroup_name: string;
    role?: string;
    extra_info?: string;
    inv_code?: string;
    subgroups: SubgroupInfo[];
}

export interface UserInfo {
    id: number
    username: string
    email: string
    role: string
}

export interface GroupInfoStructure {
    username: string;
    group_structure: GroupInfo[];
}

export interface Participant {
    id: number
    username: string
    email: string
}

export interface CompositionInfo {
    id: number
    name: string
    author: string
    files: any[]
}

export interface EventInfo {
    event_id: number
    parent_group: number
    name: string
    extra_info?: string
    date_start: string
    date_end: string
    location: string
    type: string
    set_list?: CompositionInfo[]
    participants: Participant[]
}

export interface EventCreate {
    name: string
    date_start: string
    date_end: string
    location: string
    extra_info?: string
    type: string
    parent_group: number
    group_ids: number[]
    user_emails: string[]
    composition_ids: number[]
}

export interface ForumMessageCreate {
    title: string;
    content: string;
    parent_group: number
    group_id: number
    user_ids: number[];
}


export interface Alert {
    id: number;
    title: string;
    content: string;
    parent_group: number;
    group_ids: number[];
    recipients: number[];
  }
  