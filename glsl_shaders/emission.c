#version 330


#line 1

in wparms
{
    vec4 pos;
    vec3 normal;
    vec4 color;
    vec2 texcoord0;
    noperspective in vec3 edgedist;
    flat in int edgeflags;
    float selected;
} fsIn;

layout(std140) uniform glH_Material
{
    vec3            ambient_color;
    vec3            diffuse_color;
    vec3            emission_color;
    vec3            specular_color;
    vec3            metallic_color;
    float           metal;
    float           material_alpha;
    float           material_alpha_parallel;
    float           roughness;
    float           diffuse_roughness;
    float           ior;
    float           reflection;
    float           coat_intensity;
    float           coat_roughness;
    int             specular_model;
    int             coat_spec_model;
    float           specular_tint;

    bool            use_geo_color;
    bool            use_packed_color;

    bool            has_textures;
    bool            has_diffuse_map;
    bool            has_spec_map;
    bool            has_opacity_map;
    bool            has_emission_map;
    bool            has_normal_map;
    bool            has_rough_map;
    bool            has_displace_map;
    bool            has_occlusion_map;
    bool            has_metallic_map;
    bool            has_coat_int_map;
    bool            has_coat_rough_map;
    bool            has_reflection_int_map;
    bool            has_reflect_map;
    
    ivec4           diffuse_udim_area;
    ivec4           spec_udim_area;
    ivec4           opacity_udim_area;
    ivec4           emission_udim_area;
    ivec4           normal_udim_area;
    ivec4           rough_udim_area; 
    ivec4           displace_udim_area;
    ivec4           occlusion_udim_area;
    ivec4           metallic_udim_area;
    ivec4           coat_int_udim_area;
    ivec4           coat_rough_udim_area;
    ivec4           reflection_udim_area;

    bool            has_diffuse_uv_xform;
    bool            has_spec_uv_xform;
    bool            has_opacity_uv_xform;
    bool            has_emission_uv_xform;
    bool            has_normal_uv_xform;
    bool            has_rough_uv_xform;
    bool            has_displace_uv_xform;
    bool            has_occlusion_uv_xform;
    bool            has_metallic_uv_xform;
    bool            has_coat_int_uv_xform;
    bool            has_coat_rough_uv_xform;
    bool            has_reflect_uv_xform;
    mat3            diffuse_uv_xform;
    mat3            spec_uv_xform;
    mat3            opacity_uv_xform;
    mat3            emission_uv_xform;
    mat3            normal_uv_xform;
    mat3            rough_uv_xform;
    mat3            displace_uv_xform;
    mat3            occlusion_uv_xform;
    mat3            metallic_uv_xform;
    mat3            coat_int_uv_xform;
    mat3            coat_rough_uv_xform;
    mat3            reflect_uv_xform;
    
    bool            has_env_map;
    vec3            envScale;
    mat3            envRotate;

    vec2            normalMapScaleShift;
    vec2            normalMapScale;
    vec3            normalMapXYZScale;
    int             normal_map_type; // space: 0=tangent, 1=world  
    int             normal_map_ncomps; // 2 or 3 component

    int             displace_space;
    float           displace_scale;
    float           displace_offset;
    float           displace_quality;
    bool            displace_y_up; // vs. z-up

    bool            invert_opacitymap;
    bool            use_emission_matcap;

    bool            invert_roughmap;
    vec4            rough_comp;
    
    vec4            occlusion_comp;
    vec4            metallic_comp;
    vec4            coat_int_comp;
    vec4            coat_rough_comp;
    vec4            opacity_comp;

    bool            reflection_as_ior;
    vec4            reflection_comp;
};

vec4  HOUsampleDiffuseMap(vec2 tx);
vec3  HOUsampleEmissionMap(vec2 tx);
float HOUsampleOpacityMap(vec2 tx, bool invert, vec4 comp);

#if MAX_TEXTURE_SAMPLERS >= 32
// can only do occlusion if the #texture units supports it
uniform sampler2D glH_OcclusionMap;
uniform sampler2DArray glH_OcclusionArrayMap;
uniform sampler2D glH_MetallicMap;
uniform sampler2DArray glH_MetallicArrayMap;
vec4 HOUsampleGenericMap(vec2 coords,
                         sampler2D reg_map,
                         sampler2DArray array_map,
                         ivec4 udim_area,
                         bool xform_uvs,
                         mat3 uv_xform);
#endif

uniform int glH_LightingEnabled;
uniform int glH_MaterialPass;
uniform bool  glH_HasSceneEnvMap;
uniform samplerCube glH_EnvMap;
uniform float glH_SceneIOR;
uniform float glH_Specular;

void  HOUlightingModel(vec3 P, vec3 nN,
                       vec3 m_amb,
                       vec3 m_diff,
                       vec3 m_spec,
                       vec3 m_metal,
                       inout vec3 lAmb,
                       inout vec3 lDiff,
                       inout vec3 lSpec,
                       float rough,
                       float diff_rough,
                       float ior,
                       float metal,
                       int spec_model,
                       float alpha);

void HOUassignOutputs(vec3 point_color,
                      vec3 emit_color,
                      vec3 metal_color,
                      vec3 amb_color,
                      vec3 diff_color,
                      vec3 spec_color,
                      float alpha,
                      float emit_alpha,
                      float rough,
                      float diff_rough,
                      float ior,
                      float metal,
                      float coat_intensity,
                      float coat_rough,
                      vec4 wire,
                      vec3 nN,
                      float depth,
                      float selected,
                      int lighting_model,
                      int coat_model);
vec4 HOUwireColor(vec3 edges, int edgeflags, float selected);
float HOUfresnel(float alpha_perp, float alpha_para, vec3 nN, vec3 p);
float HOUreflectionIOR(vec3 eye, vec3 n, float ior_surface, float ior_scene);

void HOUapplyLightMaps(inout vec3 mspec, inout float rough,
                       bool has_spec_map, vec2 uv,
                       bool invert_rough, vec4 rough_comp);

vec4 HOUenvmapReflect(samplerCube map, vec3 nN, vec3 p, mat3 envRotate,
                      vec3 envScale, float r, bool correct, vec3 correctvec);
vec3 HOUapplyNormalMap(vec3 P, vec3 N, vec2 uv, bool use_tangent, vec3 tn, vec3 bt);
vec3 HOUfrontFacing(vec3 n, vec3 p);

uniform float glH_Ambient;

void main()
{
    vec3 nN, p;
    vec3 lspec, ldiff, lamb, ptcol;
    vec4 tex;
    vec3 mspec, memit;
    vec3 envmap;
    vec4 wire;

    float rough, alpha, mtl, diff_rough;

    p = fsIn.pos.xyz / fsIn.pos.w;
    ptcol = fsIn.color.rgb * fsIn.color.a;
    nN = fsIn.normal;
    rough = roughness;
    diff_rough = diffuse_roughness;

    lamb  = vec3(0.0);
    ldiff = vec3(1.0);
    lspec = vec3(0.0);
    envmap = vec3(0.0);
    mtl = metal;

    // read in texture maps 
    if(has_diffuse_map)
        tex = HOUsampleDiffuseMap(fsIn.texcoord0);
    else
        tex = vec4(1.0);

    if(has_opacity_map)
        tex.a *= HOUsampleOpacityMap(fsIn.texcoord0, invert_opacitymap,
                                     opacity_comp);

    if(has_emission_map)
        memit = HOUsampleEmissionMap(fsIn.texcoord0);
    else
        memit = vec3(0.0);
        
    // Use this as the final color output
    memit = vec3(0.0, 1.0, 0.0);

    lspec = vec3(0.0);
    // ldiff = diffuse_color;
    ldiff = vec3(0.0);
    // lamb = ambient_color;
    lamb = vec3(0.0);
    alpha = fsIn.color.a * tex.a;

    // blend in wire color around the edges of polygons, if wire-over-shaded
    // active
    wire = HOUwireColor(fsIn.edgedist,fsIn.edgeflags,fsIn.selected);

    // Write out the data to either the forward renderer framebuffer or the
    // deferred framebuffer (glH_MaterialPass==1).
    HOUassignOutputs(ptcol,
                     emission_color + memit,
                     metallic_color,
                     lamb* tex.rgb,
                     ldiff* tex.rgb,
                     lspec + envmap,
                     alpha,
                     wire.a,
                     rough,
                     diff_rough,
                     ior,
                     mtl,
                     coat_intensity,
                     coat_roughness,
                     wire,
                     nN,
                     p.z,
                     fsIn.selected,
                     specular_model, coat_spec_model);
}
