<template>
  <br />
  <img :src="src" alt="Picture" class="img-fluid" />
  <div class="col-lg-12">
    <button type="button" id="btn-pic-inp" class="btn btn-success" @click="browse()">Image</button>
  </div>
  <input type="file" accept="image/*" class="invisible" ref="file" @change="change" />
</template>
<script>
export default {
  emits: ["input", "src"],
  props: {
    value: File
  },
  data() {
    return {
      file: null,
      src: "../src/assets/picture-input.png"
    }
  },
  methods: {
    browse() {
      this.$refs.file.click()
    },
    change(e) {
      this.file = e.target.files[0]
      this.$emit("input", this.file)
      let reader = new FileReader()
      reader.readAsDataURL(this.file)
      reader.onload = (e) => {
        let src = (this.src = e.target.result)
        this.$emit("src", src)
      }
    }
  }
}
</script>
<style>
.img-fluid {
  max-width: 30%;
  margin-bottom: 2rem;
}
</style>
