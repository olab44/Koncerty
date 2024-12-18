interface GroupInfo {
    group_id: number;
    group_name: string;
    role: string;
    subgroups?: SubgroupInfo[];
}

interface SubgroupInfo {
    subgroup_id: number;
    subgroup_name: string;
    role: string;
}

interface GroupInfoStructure {
    username: string;
    group_structure: GroupInfo[];
}

export {GroupInfo, SubgroupInfo, GroupInfoStructure}