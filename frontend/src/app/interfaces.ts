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
    role: string;
    extra_info?: string;
    inv_code?: string;
    subgroups: SubgroupInfo[];
}

export interface GroupInfoStructure {
    username: string;
    group_structure: GroupInfo[];
}
