
## From the forums:

resource: https://discuss.streamlit.io/t/how-does-streamlit-component-create-a-key-session-state-variable/35409

```
Hi everyone,

I think it would be great to explain how I managed to make this work eventually.

The answer to my question was to use the abstract class StreamlitComponentBase to build my component as a class.

import {
  Streamlit, StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ComponentProps, useEffect, useState } from "react"
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from "@mui/material/Select"
import { Box, FormControl, InputLabel } from "@mui/material"

class SelectImage extends StreamlitComponentBase {

  state = { back: [], options: this.props.args.options, images: this.props.args.images, value: this.props.args.default}

  componentDidMount() {
    const back: any[] = [];
    for (let i=0; i < this.state.options.length; i++) {
      back.push({option: this.state.options[i], image: this.state.images[i]});
    }
    this.setState((prev, state) => ({
      back: back,
    }), () => Streamlit.setComponentValue(this.state.value))
  }

  handleChange = (event: SelectChangeEvent) => {
    this.setState((prev, state) => ({
      value: event.target.value
    }),
      () => Streamlit.setComponentValue(this.state.value)
    )
  }

  render = () => {
    if (this.props.args["label"] !== "") {
      return (
        <Box sx={{ minWidth: 50 , marginTop: 2}}>
          <FormControl fullWidth>
            <InputLabel id="image-select-label">{this.props.args["label"]}</InputLabel>
            <Select
              labelId="image-select-label"
              id="image-select"
              value={this.state.value}
              label="Image"
              onChange={this.handleChange}
            >
              {this.state.back.map(({ image, option }) => (
                <MenuItem value={option}><img alt={option} src={image} height={"100px"} width={"100px"}/></MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      );
    } else {
      return (
        <Box sx={{ minWidth: 50 , marginTop: 2}}>
          <FormControl fullWidth>
            <Select
              labelId="image-select-label"
              id="image-select"
              value={this.state.value}
              onChange={this.handleChange}
            >
              {this.state.back.map(({ image, option }) => (
                <MenuItem value={option}><img alt={option} src={image} height={"100px"} width={"100px"}/></MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      );
    }
  }

}

export default withStreamlitConnection(SelectImage)

As you can see, I exchanged the useState function by a state class attribute. I used the componentDidMount to initialize the value of my component in the session state.

I rewrote the handleChange function as a class method sending the state value variable to Streamlit !

Eventually, when I instantiate with a for loop multiple custom component, it gives me the path corresponding to the first image as you can see below (compared to the None value before).
```

What ChatGPT suggested to make of `quill.tsx`, seems not correct though

```
import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection
} from "streamlit-component-lib";
import React, { useState } from "react"
import ReactQuill from "react-quill"
import ResizeObserver from "resize-observer-polyfill"
import katex from "katex"

import "katex/dist/katex.min.css"
import "quill/dist/quill.snow.css"

interface QuillProps extends ComponentProps {
  args: any
}

class Quill extends StreamlitComponentBase {
  state = {
    text: this.props.args.defaultValue
  }

  handleChange = (content: string, delta: any, source: any, editor: any) => {
    this.setState({ text: content }, () => {
      Streamlit.setComponentValue(this.state.text)
    })
  }

  render = () => {
    const { args } = this.props

    return (
      <div ref={this.divRef}>
        <ReactQuill
          defaultValue={args.defaultValue}
          modules={{
            toolbar: args.toolbar,
            history: args.history,
          }}
          placeholder={args.placeholder}
          preserveWhitespace={args.preserveWhitespace}
          readOnly={args.readOnly}
          onChange={this.handleChange}
        />
      </div>
    )
  }
}

export default withStreamlitConnection(Quill)
```
